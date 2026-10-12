#!/usr/bin/env python3
"""Architecture guardrail checker (stack-neutral: .ts .tsx .js .jsx .mjs .py).

Config: docs/architecture/modules.json. Enforces:
  1. every module directory under source_root is registered
  2. cross-module imports follow allowed_dependencies (dependency direction)
  3. cross-module imports go through the module's public entry point only
  4. no circular dependencies between modules (configured and observed)
  5. forbidden import patterns
Exit codes: 0 pass, 1 violations, 2 configuration error.
"""
from __future__ import annotations
import argparse, ast, json, re, sys
from pathlib import Path

EXTS = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".py"}
SKIP_DIRS = {"node_modules", "__pycache__", "dist", "build", ".venv"}
JS_RE = re.compile(
    r"""(?:\bimport\s+(?:[^'";]*?\s+from\s+)?|\bexport\s+[^'";]*?\s+from\s+|\brequire\(\s*|\bimport\(\s*)['"]([^'"]+)['"]"""
)
def extract_imports(text: str, ext: str, file=None, cfg=None, src_root=None):
    if ext == ".py":
        imports = []
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Import):
                imports.extend(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                parent = '.' * node.level + (node.module or '')
                imports.append(parent)
                for alias in node.names:
                    if alias.name == '*':
                        continue
                    spec = parent + ('' if parent.endswith('.') else '.') + alias.name
                    # A from-list name may be a public symbol or a submodule.
                    # Resolve every alias and inspect submodules that exist on disk.
                    res = resolve(spec, file, cfg, src_root) if file else None
                    if res:
                        target, sub = res
                        candidate = src_root.joinpath(target, *sub)
                        if candidate.is_dir() or candidate.with_suffix('.py').is_file():
                            imports.append(spec)
        return imports
    return JS_RE.findall(text)


def strip_ext(parts):
    if not parts:
        return parts
    last = parts[-1]
    for e in EXTS:
        if last.endswith(e):
            return parts[:-1] + (last[: -len(e)],)
    return parts


def resolve(spec, file: Path, cfg, src_root: Path):
    """Return (target_module, sub_path_parts) when spec points into source_root, else None."""
    if file.suffix == ".py":
        if spec.startswith("."):
            dots = len(spec) - len(spec.lstrip("."))
            base = file.parent
            for _ in range(dots - 1):
                base = base.parent
            rest = spec.lstrip(".")
            target = base.joinpath(*rest.split(".")) if rest else base
        else:
            prefix = cfg["source_root"].strip("/").replace("/", ".")
            if spec == prefix or spec.startswith(prefix + "."):
                rest = spec[len(prefix):].lstrip(".")
                target = src_root.joinpath(*rest.split(".")) if rest else src_root
            else:
                return None
    else:
        if spec.startswith("."):
            target = (file.parent / spec).resolve()
        else:
            for alias in cfg.get("aliases", ["@modules/"]):
                if spec.startswith(alias):
                    target = (src_root / spec[len(alias):]).resolve()
                    break
            else:
                return None
    try:
        rel = target.resolve().relative_to(src_root.resolve())
    except ValueError:
        return None
    if not rel.parts:
        return None
    sub = rel.parts[1:]
    if file.suffix != ".py":
        sub = strip_ext(sub)
    return rel.parts[0], sub


def find_cycle(graph):
    state, stack = {}, []

    def dfs(n):
        state[n] = 1
        stack.append(n)
        for m in sorted(graph.get(n, ())):
            if state.get(m) == 1:
                return stack[stack.index(m):] + [m]
            if state.get(m) is None:
                c = dfs(m)
                if c:
                    return c
        stack.pop()
        state[n] = 2
        return None

    for n in sorted(graph):
        if state.get(n) is None:
            c = dfs(n)
            if c:
                return c
    return None


def check(root: Path, config_path: Path):
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    modules = cfg["modules"]
    entry_names = set(cfg.get("public_entry_names", ["index", "__init__"]))
    public_dirs = set(cfg.get("public_dirs", ["public"]))
    violations = []

    cfg_graph = {m: set(v.get("allowed_dependencies", [])) for m, v in modules.items()}
    for m, deps in cfg_graph.items():
        for d in sorted(deps):
            if d not in modules:
                violations.append(f"config: module '{m}' allows unknown module '{d}'")
    cyc = find_cycle(cfg_graph)
    if cyc:
        violations.append("config: circular allowed_dependencies: " + " -> ".join(cyc))

    src_root = root / cfg["source_root"]
    if not src_root.is_dir():
        return violations + [f"configured source directory missing: {cfg['source_root']}"], 0
    for directory in sorted(src_root.iterdir()):
        if directory.is_dir() and directory.name not in modules and directory.name not in SKIP_DIRS:
            violations.append(f"{directory.relative_to(root)}: module directory is not registered in modules.json")
    observed = {m: set() for m in modules}
    reported_unregistered = set()
    scanned = 0
    for path in sorted(src_root.rglob("*")):
        if not path.is_file() or path.suffix not in EXTS:
            continue
        rel = path.relative_to(src_root)
        if any(p in SKIP_DIRS for p in rel.parts) or len(rel.parts) < 2:
            continue
        module = rel.parts[0]
        scanned += 1
        if module not in modules:
            if module not in reported_unregistered:
                reported_unregistered.add(module)
                violations.append(f"{cfg['source_root']}/{module}: module directory is not registered in modules.json (needs ADR + tech-owner approval)")
            continue
        text = path.read_text(encoding="utf-8")
        where = path.relative_to(root)
        try:
            imports = extract_imports(text, path.suffix, path, cfg, src_root)
        except SyntaxError as e:
            violations.append(f"{where}:{e.lineno}: Python syntax error: {e.msg}")
            continue
        for spec in imports:
            for rule in cfg.get("forbidden_imports", []):
                applies = rule.get("applies_to_modules")
                if re.search(rule["pattern"], spec) and (not applies or module in applies):
                    violations.append(f"{where}: forbidden import '{spec}' - {rule['reason']}")
            res = resolve(spec, path, cfg, src_root)
            if not res:
                continue
            target, sub = res
            if target == module:
                continue
            if target not in modules:
                violations.append(f"{where}: imports unregistered module '{target}'")
                continue
            observed[module].add(target)
            if target not in cfg_graph[module]:
                violations.append(f"{where}: module '{module}' may not depend on '{target}' (see allowed_dependencies)")
            elif not (len(sub) == 0 or (len(sub) == 1 and sub[0] in entry_names) or sub[0] in public_dirs):
                violations.append(f"{where}: deep import '{spec}' - import '{target}' only through its public entry point")
    cyc = find_cycle(observed)
    if cyc:
        violations.append("observed circular dependency: " + " -> ".join(cyc))
    if scanned == 0 and cfg.get('allow_empty_bootstrap') is not True:
        violations.append("no supported source files; an existing empty source tree requires allow_empty_bootstrap: true")
    return violations, scanned


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="docs/architecture/modules.json")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    cfgp = root / a.config
    try:
        violations, scanned = check(root, cfgp)
    except (OSError, ValueError, KeyError) as e:
        print(f"CONFIG ERROR: {e}")
        return 2
    for v in violations:
        print("VIOLATION:", v)
    if violations:
        print(f"architecture check FAILED: {len(violations)} violation(s), {scanned} file(s) scanned")
        return 1
    print(f"architecture check passed: {scanned} source file(s) scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
