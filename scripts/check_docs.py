#!/usr/bin/env python3
"""Documentation and consistency checker.
Checks: required files exist; markdown links resolve; backticked repo paths resolve; gates 0-10 documented;
workflow has all 11 steps; environment names consistent; seven blocks in prompt template; wizard covers
all 16 topics; AGENTS.md/CLAUDE.md point at canonical docs.
--strict-setup additionally fails while placeholder owners/values remain (use at Gate 4)."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

REQUIRED = """README.md AGENTS.md CLAUDE.md Makefile .gitignore .editorconfig .secrets-allowlist .pre-commit-config.yaml
.github/CODEOWNERS .github/pull_request_template.md .github/dependabot.yml .github/workflows/governance.yml
.github/ISSUE_TEMPLATE/bug_report.md .github/ISSUE_TEMPLATE/task.md
docs/wizard/questions.json docs/wizard/WIZARD.md docs/decisions/README.md
docs/governance/engineering-standard.md docs/governance/workflow.md docs/governance/gates.md docs/governance/gate-log.md
docs/governance/definition-of-ready-done.md docs/governance/skill-guidance.md docs/governance/change-impact-checklist.md
docs/governance/team-coordination.md docs/governance/git-environment-governance.md docs/governance/exception-process.md
docs/governance/continuous-improvement.md docs/governance/enforcement-status.md
docs/architecture/architecture-decision-guide.md docs/architecture/quality-attributes.md docs/architecture/guardrails.md
docs/architecture/modules.json docs/architecture/adr/0000-template.md docs/architecture/adr/0001-adopt-ai-segs.md
docs/requirements/README.md docs/api/README.md docs/security/security-baseline.md docs/testing/testing-strategy.md
docs/deployment/ci-cd.md docs/deployment/environments.md docs/deployment/release-checklist.md docs/deployment/stack-examples.md
docs/operations/README.md docs/operations/runbooks/incident-response.md docs/operations/runbooks/failed-deployment-rollback.md
docs/operations/runbooks/backup-restore.md docs/operations/runbooks/performance-degradation.md
docs/operations/runbooks/security-incident.md docs/operations/runbooks/dependency-failure.md docs/operations/runbooks/emergency-hotfix.md
docs/design-system/design-system-governance.md docs/roadmap/mvp-roadmap.md docs/roadmap/feature-register.md
docs/team/roles-and-ownership.md docs/registers/risk-log.md docs/registers/technical-debt-register.md
docs/registers/defect-log.md docs/registers/improvement-register.md docs/examples/end-to-end-feature.md
prompts/seven-block-prompt.md prompts/wizard-facilitator-prompt.md prompts/examples/FEAT-003-cancel-order.md prompts/tasks/README.md
templates/README.md templates/change-request.md templates/exception-request.md templates/impact-analysis.md
templates/feature.md templates/runbook.md templates/incident-postmortem.md templates/release-notes.md templates/threat-model.md
scripts/verify_all.sh scripts/configure_branch_protection.sh src/README.md tests/governance/test_guardrails.py""".split()

GENERATED_OK = {"docs/decisions/project-profile.md"}
SKIP_TOKENS = ("<", "*", "{", "NNN", "YYYY", "XXX", "...")
PATH_RE = re.compile(r"`((?:docs|scripts|templates|prompts|tests|src|\.github)/[^`\s]*)`")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
ENVS = ["Dev", "QA", "Staging", "Production"]
STEPS = ["Understand", "Clarify", "Assess impact", "Plan", "Approve", "Implement", "Verify", "Review", "Integrate", "Release", "Learn"]
BLOCKS = ["Role", "Context", "Objective", "Scope and non-goals", "Constraints", "Acceptance criteria", "Verification and handoff"]


def strip_code(text: str):
    """Yield (lineno, line) outside fenced code, with inline code removed (but keep backtick paths separately)."""
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield n, line


def check(root: Path, strict_setup: bool = False):
    errs = []
    for f in REQUIRED:
        if not (root / f).exists():
            errs.append(f"missing required file: {f}")
    md_files = [p for p in root.rglob("*.md") if ".git" not in p.parts]
    for p in md_files:
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding="utf-8")
        for n, line in strip_code(text):
            no_inline = re.sub(r"`[^`]*`", "", line)
            for target in LINK_RE.findall(no_inline):
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                t = target.split("#")[0]
                if t and not (p.parent / t).exists():
                    errs.append(f"{rel}:{n}: broken link -> {target}")
            for ref in PATH_RE.findall(line):
                if any(tok in ref for tok in SKIP_TOKENS) or ref in GENERATED_OK:
                    continue
                if not (root / ref.rstrip("/")).exists():
                    errs.append(f"{rel}:{n}: referenced path does not exist -> {ref}")

    def read(rel):
        p = root / rel
        return p.read_text(encoding="utf-8") if p.exists() else ""

    gates = read("docs/governance/gates.md")
    for g in range(11):
        if not re.search(rf"\bGate {g}\b", gates):
            errs.append(f"gates.md: Gate {g} not documented")
    wf = read("docs/governance/workflow.md")
    for s in STEPS:
        if s not in wf:
            errs.append(f"workflow.md: step '{s}' missing")
    for rel in ("docs/governance/git-environment-governance.md", "docs/deployment/environments.md",
                "docs/deployment/ci-cd.md", "docs/deployment/release-checklist.md"):
        t = read(rel)
        for e in ENVS:
            if e not in t:
                errs.append(f"{rel}: environment '{e}' not mentioned (Dev -> QA -> Staging -> Production must be consistent)")
    pt = read("prompts/seven-block-prompt.md")
    for i, b in enumerate(BLOCKS, 1):
        if f"## {i}. {b}" not in pt:
            errs.append(f"prompts/seven-block-prompt.md: block '{i}. {b}' missing")
    qp = root / "docs/wizard/questions.json"
    if qp.exists():
        data = json.loads(qp.read_text(encoding="utf-8"))
        topics = {str(q["topic"]) for q in data["questions"]}
        for t in range(1, 17):
            if str(t) not in topics:
                errs.append(f"wizard: topic {t} has no question")
        for q in data["questions"]:
            if q["options"] and q.get("default") not in {o["key"] for o in q["options"]}:
                errs.append(f"wizard: {q['id']} default is not one of its options")
    for rel in ("AGENTS.md", "CLAUDE.md"):
        t = read(rel)
        for needle in ("docs/governance/workflow.md", "prompts/seven-block-prompt.md"):
            if needle not in t and rel == "AGENTS.md":
                errs.append(f"{rel}: must link canonical doc {needle}")
    if "AGENTS.md" not in read("CLAUDE.md"):
        errs.append("CLAUDE.md: must import AGENTS.md (one canonical rule set)")
    if strict_setup:
        co = read(".github/CODEOWNERS")
        if "@your-org" in co:
            errs.append(".github/CODEOWNERS still contains @your-org placeholders (Gate 4)")
        mj = read("docs/architecture/modules.json")
        if "@your-org" in mj:
            errs.append("docs/architecture/modules.json still contains @your-org owner placeholders (Gate 4)")
        if not (root / "docs/decisions/project-profile.md").exists():
            errs.append("docs/decisions/project-profile.md missing: run the wizard (Gate 0-3)")
    return errs, len(md_files)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--strict-setup", action="store_true")
    a = ap.parse_args(argv)
    errs, n = check(Path(a.root).resolve(), a.strict_setup)
    for e in errs:
        print("DOCS:", e)
    if errs:
        print(f"docs check FAILED: {len(errs)} problem(s) across {n} markdown file(s)")
        return 1
    print(f"docs check passed: {n} markdown file(s), required files, links, paths, gates, workflow, environments, wizard")
    return 0


if __name__ == "__main__":
    sys.exit(main())
