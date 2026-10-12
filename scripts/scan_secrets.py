#!/usr/bin/env python3
"""Lightweight secret scanner (fallback/pre-commit layer; use a dedicated scanner such as gitleaks in CI too).
Never prints secret values. Allowlist: .secrets-allowlist (one repo-relative path per line)."""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

RULES = {
    "aws-access-key-id": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private-key-block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY"),
    "github-token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "slack-token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "hardcoded-credential": re.compile(r"""(?i)(api[_-]?key|secret|passwd|password|token)\s*[:=]\s*['"][A-Za-z0-9/+_\-]{16,}['"]"""),
}
SKIP_DIRS = {".git", "node_modules", "__pycache__", "dist", "build", ".venv"}


def scan(root: Path):
    allow = set()
    af = root / ".secrets-allowlist"
    if af.exists():
        allow = {l.strip() for l in af.read_text().splitlines() if l.strip() and not l.startswith("#")}
    findings, count = [], 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        rel = p.relative_to(root).as_posix()
        if rel in allow or p.stat().st_size > 1_000_000:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        count += 1
        for i, line in enumerate(text.splitlines(), 1):
            for name, rx in RULES.items():
                if rx.search(line):
                    findings.append((rel, i, name))
    return findings, count


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    a = ap.parse_args(argv)
    findings, count = scan(Path(a.root).resolve())
    for rel, line, name in findings:
        print(f"SECRET? {rel}:{line} rule={name}")
    if findings:
        print(f"secret scan FAILED: {len(findings)} finding(s) in {count} file(s)")
        return 1
    print(f"secret scan passed: {count} file(s) scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
