#!/usr/bin/env python3
"""Validate seven-block task prompts (prompts/tasks/*.md and prompts/examples/*.md).
Rules: header has Task-ID and an explicit Gate-5 approval; seven numbered blocks present, in order,
non-empty, no {{placeholders}}/TBD/TODO; acceptance criteria has >= 2 items."""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

BLOCKS = ["Role", "Context", "Objective", "Scope and non-goals", "Constraints",
          "Acceptance criteria", "Verification and handoff"]
HEAD = re.compile(r"^##\s+(\d)\.\s+(.+?)\s*$", re.M)
TASK_ID = re.compile(r"^Task-ID:\s*(FEAT|BUG|CHG|TASK|DEBT)-\d+\s*$", re.M)
APPROVAL = re.compile(r"^Gate-5-approval:\s*Approved by\s+\S.*\d{4}-\d{2}-\d{2}", re.M)
BAD = re.compile(r"\{\{|\bTBD\b|\bTODO\b|\bFIXME\b")


def check_text(text: str):
    errs = []
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    if not TASK_ID.search(text):
        errs.append("missing 'Task-ID: <FEAT|BUG|CHG|TASK|DEBT>-<number>'")
    if not APPROVAL.search(text):
        errs.append("missing 'Gate-5-approval: Approved by <name> <YYYY-MM-DD>' (task not approved)")
    heads = list(HEAD.finditer(text))
    found = [(int(m.group(1)), m.group(2)) for m in heads]
    expected = [(i + 1, b) for i, b in enumerate(BLOCKS)]
    if found != expected:
        errs.append(f"blocks must be exactly, in order: {', '.join(f'{n}. {t}' for n, t in expected)}")
        return errs
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end():end].strip()
        name = BLOCKS[i]
        if len(body) < 20:
            errs.append(f"block '{name}' is empty or too short")
        if BAD.search(body):
            errs.append(f"block '{name}' contains a placeholder/TBD/TODO")
        if name == "Acceptance criteria" and len(re.findall(r"^\s*(?:[-*]|\d+\.)\s+\S", body, re.M)) < 2:
            errs.append("acceptance criteria needs at least 2 listed, testable items")
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--root", default=".")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    files = [Path(f) for f in a.files] or sorted(
        list((root / "prompts/tasks").glob("*.md")) + list((root / "prompts/examples").glob("*.md")))
    files = [f for f in files if f.name.lower() != "readme.md"]
    bad = 0
    for f in files:
        errs = check_text(f.read_text(encoding="utf-8"))
        for e in errs:
            print(f"{f}: {e}")
        bad += bool(errs)
    if bad:
        print(f"task prompt check FAILED: {bad} file(s)")
        return 1
    print(f"task prompt check passed: {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
