#!/usr/bin/env python3
"""Render docs/wizard/WIZARD.md from docs/wizard/questions.json (single source of truth).
  render_wizard.py          write WIZARD.md
  render_wizard.py --check  fail if WIZARD.md is out of date"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

HEADER = """# Guided Discovery Wizard

> GENERATED from `docs/wizard/questions.json` by `scripts/render_wizard.py`. Do not edit by hand; edit the JSON and re-run the script.

The wizard records proposals for human approval, **one question at a time**. For each question you get: why it matters, the options with trade-offs, a recommended default, and the choice to accept or override it.

How to run it:

- **With Claude (recommended for founders):** paste `prompts/wizard-facilitator-prompt.md` into a chat with this repository attached.
- **In a terminal:** `python scripts/wizard.py` (interactive) or `python scripts/wizard.py --defaults` (writes every recommended default, flagged as an unapproved assumption).

For option questions, type only the option letter. Type `o` to supply an alternative and reason when none fits (for example repository/CLI tooling with no hosted application or database). Alternatives remain proposals pending the responsible human's gate approval.

Progress is atomically saved after each answer to the JSON state under `docs/decisions/`. Run `python scripts/wizard.py --resume` after interruption. A completed profile is written once to `docs/decisions/project-profile.md`; existing state/profile files are never silently overwritten. Archive both explicitly to start a new discovery session, keeping any gate approvals for audit. If questions changed, reconcile saved answers manually before resuming. A choice is only *approved* when the responsible person signs the matching gate in `docs/governance/gate-log.md`. Silent defaults are not approvals.

"""


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def render(data) -> str:
    qs = sorted(data["questions"], key=lambda q: q["id"])
    out = [HEADER, "## Overview: decide now vs. defer\n",
           "| ID | Topic | Gate | Can defer? |", "|---|---|---|---|"]
    for q in qs:
        out.append(f"| {q['id']} | {q['topic']}. {data['topics'][str(q['topic'])]} | {q['gate']} | {'Yes' if q['can_defer'] else 'No - needed before the gate'} |")
    out.append("\nQuestions marked *Yes* may be answered with the default and revisited later; record the deferral so it is a visible assumption, not a silent decision.\n")
    out.append("## Questions\n")
    for q in qs:
        out.append(f"### {q['id']} - Topic {q['topic']}: {data['topics'][str(q['topic'])]}\n")
        out.append(f"**Question:** {q['question']}\n")
        out.append(f"**Why it matters:** {q['why']}\n")
        if q["options"]:
            out.append("| Key | Option | Trade-off |\n|---|---|---|")
            for o in q["options"]:
                out.append(f"| {o['key']} | {o['label']} | {o['tradeoff']} |")
            d = next(o for o in q["options"] if o["key"] == q["default"])
            out.append(f"\n**Recommended default:** {d['key']} - {d['label']}\n")
        else:
            out.append("**Answer format:** free text." + (f" Example: *{q['example']}*" if q.get("example") else "") + " No default is possible; this must come from you.\n")
        out.append(f"**Needed by:** Gate {q['gate']}. **Can be deferred:** {'Yes' if q['can_defer'] else 'No'}.\n")
    return "\n".join(out).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    text = render(load(root / "docs/wizard/questions.json"))
    target = root / "docs/wizard/WIZARD.md"
    if a.check:
        if not target.exists() or target.read_text(encoding="utf-8") != text:
            print("WIZARD.md is out of date: run python scripts/render_wizard.py")
            return 1
        print("wizard render is in sync with questions.json")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
