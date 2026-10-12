#!/usr/bin/env python3
"""Validate docs/roadmap/feature-register.md (scope governance)."""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

COLS = ["ID", "Title", "User value", "MVP", "Priority", "Modules", "Quality attrs", "Depends on",
        "Test requirements", "Owner", "Approval", "Status", "Evidence"]
MVPS = {"MVP1", "MVP2", "MVP3", "Later", "Non-goal"}
APPROVALS = {"Pending", "Approved", "Rejected"}
STATUSES = {"Proposed", "Approved", "Ready", "In-Progress", "In-Review", "Verified", "Released", "Deferred", "Rejected"}
NEEDS_APPROVAL = {"Approved", "Ready", "In-Progress", "In-Review", "Verified", "Released"}
NEEDS_EVIDENCE = {"Verified", "Released"}
ID_RE = re.compile(r"^FEAT-\d{3,}$")


def check_text(text: str):
    errs, seen, in_table = [], set(), False
    headers, rows, separator = 0, 0, False
    if not text.strip():
        return ['feature register is empty']
    for n, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):
            in_table = in_table and False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "ID":
            headers += 1
            separator = False
            if cells != COLS:
                errs.append(f"line {n}: header must be exactly: {' | '.join(COLS)}")
            in_table = True
            continue
        if not in_table:
            continue
        if not separator:
            separator = True
            if len(cells) == len(COLS) and all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                continue
            errs.append(f"line {n}: missing or malformed table separator")
        rows += 1
        if len(cells) != len(COLS):
            errs.append(f"line {n}: expected {len(COLS)} columns, found {len(cells)}")
            continue
        r = dict(zip(COLS, cells))
        for col in ['Title', 'User value', 'Priority', 'Modules', 'Test requirements', 'Owner']:
            if r[col] in ('', '-', '—', 'N/A'):
                errs.append(f"line {n}: mandatory field {col} is missing")
        if r['Priority'] not in {'Must','Should','Could','Won\'t'}:
            errs.append(f"line {n}: Priority must be Must/Should/Could/Won't")
        if not ID_RE.match(r["ID"]):
            errs.append(f"line {n}: bad ID '{r['ID']}' (use FEAT-001 style)")
        if r["ID"] in seen:
            errs.append(f"line {n}: duplicate ID {r['ID']}")
        seen.add(r["ID"])
        if r["MVP"] not in MVPS:
            errs.append(f"line {n}: MVP must be one of {sorted(MVPS)}")
        if r["Approval"] not in APPROVALS:
            errs.append(f"line {n}: Approval must be one of {sorted(APPROVALS)}")
        if r["Status"] not in STATUSES:
            errs.append(f"line {n}: Status must be one of {sorted(STATUSES)}")
        if r["Status"] in NEEDS_APPROVAL and r["Approval"] != "Approved":
            errs.append(f"line {n}: {r['ID']} is '{r['Status']}' but Approval is '{r['Approval']}' (unapproved work)")
        if r['Status'] == 'Proposed' and r['Approval'] != 'Pending':
            errs.append(f"line {n}: Proposed state requires Pending approval")
        if r["Status"] in NEEDS_EVIDENCE and r["Evidence"] in ("", "-", "—"):
            errs.append(f"line {n}: {r['ID']} is '{r['Status']}' without verification evidence")
        if r['Approval'] == 'Rejected' and r['Status'] != 'Rejected' or r['Status'] == 'Rejected' and r['Approval'] != 'Rejected':
            errs.append(f"line {n}: rejected approval and status must agree")
        if r['Approval'] == 'Approved' and (r['Evidence'] in ('', '-', '—', 'N/A') or len(r['Evidence']) < 10):
            errs.append(f"line {n}: approved feature needs approval record evidence")
        if r['Approval'] == 'Approved' and re.search(r'\(name\)|<|>|@your-org|\bTBD\b',r['Owner']):
            errs.append(f"line {n}: approved feature needs a real owner")
        if r['Status'] in NEEDS_EVIDENCE and len(r['Evidence']) < 10:
            errs.append(f"line {n}: evidence must identify a test/review/release record")
    if headers != 1:
        errs.append(f"require exactly one canonical header, found {headers}")
    if headers == 1 and not separator:
        errs.append('missing table separator')
    if rows == 0 and not re.search(r'^Bootstrap-empty: yes\s*$', text, re.M):
        errs.append('zero features only allowed with Bootstrap-empty: yes before Gate 2')
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--file", default="docs/roadmap/feature-register.md")
    a = ap.parse_args(argv)
    p = Path(a.root).resolve() / a.file
    if not p.exists():
        print(f"missing {p}")
        return 1
    errs = check_text(p.read_text(encoding="utf-8"))
    for e in errs:
        print(f"{a.file}: {e}")
    if errs:
        print(f"feature register check FAILED: {len(errs)} problem(s)")
        return 1
    print("feature register check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
