#!/usr/bin/env python3
"""Interactive discovery wizard. Asks one question at a time; writes docs/decisions/project-profile.md.
  Enter = accept recommended default | letter = choose option | o = other proposal | d = defer (if allowed) | ? = repeat explanation
  --defaults = non-interactive: record every recommended default as an UNAPPROVED assumption."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_wizard import load  # noqa: E402


def show(q, topics, say):
    say(f"\n[{q['id']}] Topic {q['topic']}: {topics[str(q['topic'])]}  (needed by Gate {q['gate']})")
    say(f"Q: {q['question']}")
    say(f"Why it matters: {q['why']}")
    for o in q["options"]:
        mark = " (recommended)" if o["key"] == q.get("default") else ""
        say(f"  {o['key']}) {o['label']}{mark}\n     Trade-off: {o['tradeoff']}")
    if q['options']:
        say('  o) Other (specify)\n     Trade-off: Record a tailored proposal for human review; it does not waive the gate.')
    if q.get("example"):
        say(f"  Example: {q['example']}")


def run(data, ask=None, say=print, use_defaults=False, initial=None, save=None):
    ask = ask or input
    rows, topics = list(initial or []), data["topics"]
    for q in data["questions"]:
        if any(row[0]['id'] == q['id'] for row in rows):
            continue
        opts = {o["key"].upper(): o for o in q["options"]}
        default = q.get("default")
        if use_defaults:
            if default:
                rows.append((q, f"{default} - {opts[default]['label']}", "assumed-default"))
            else:
                rows.append((q, f"NOT ANSWERED - required before Gate {q['gate']}", "unanswered"))
            if save: save(rows)
            continue
        show(q, topics, say)
        while True:
            hint = "Enter=default, " if default else ""
            raw = ask(f"Your answer ({hint}{'o=other, ' if opts else ''}{'d=defer, ' if q['can_defer'] else ''}?=help): ").strip()
            if raw == "?":
                show(q, topics, say)
            elif raw == "" and default:
                label = opts[default]['label']
                if label.startswith('Other') or '(specify)' in label:
                    detail = ask('Please specify: ').strip()
                    if not detail:
                        say('A specific answer is required.'); continue
                    label += ': ' + detail
                rows.append((q, f"{default} - {label}", "default-accepted")); break
            elif raw.lower() == "d" and q["can_defer"]:
                rows.append((q, "DEFERRED" + (f" (working assumption: {default} - {opts[default]['label']})" if default else ""), "deferred")); break
            elif opts and raw.lower() == 'o' and 'O' not in opts:
                detail = ask('Please specify your alternative and reason: ').strip()
                if not detail:
                    say('A specific answer is required.'); continue
                rows.append((q, 'Other: ' + detail, 'chosen-other')); break
            elif opts and raw.upper() in opts:
                o = opts[raw.upper()]
                label = o["label"]
                if label.startswith("Other") or "(specify)" in label:
                    detail = ask("Please specify: ").strip()
                    if not detail:
                        say('A specific answer is required.'); continue
                    label += ": " + detail
                rows.append((q, f"{o['key']} - {label}", "chosen")); break
            elif not opts and raw:
                rows.append((q, raw, "chosen")); break
            else:
                say("Please choose one of the shown options" + ("." if opts else " or type your answer."))
        if save: save(rows)
    return rows


def render_profile(rows) -> str:
    out = ["# Project Profile (wizard output)", "",
           "> Written by `scripts/wizard.py`. Entries are **proposals** until the responsible approver signs the matching gate in `docs/governance/gate-log.md`.", "",
           "| ID | Gate | Decision | Source | Gate approval |", "|---|---|---|---|---|"]
    for q, decision, source in rows:
        decision = ' '.join(decision.replace('|', '/').splitlines())
        out.append(f"| {q['id']} | {q['gate']} | {decision} | {source} | Pending |")
    pend = [(q, s) for q, _, s in rows if s in ("assumed-default", "default-accepted", "deferred", "unanswered")]
    out += ["", "## Assumptions and open items", "",
            "Each item below is an assumption or gap, not an approved decision. Resolve it at the gate shown.", ""]
    out += [f"- {q['id']} (Gate {q['gate']}): {s}" for q, s in pend] or ["- None"]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--defaults", action="store_true")
    ap.add_argument('--resume', action='store_true', help='continue saved answers; never restart silently')
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    data = load(root / "docs/wizard/questions.json")
    target = root / 'docs/decisions/project-profile.md'
    state = root / 'docs/decisions/wizard-progress.json'
    digest = hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
    initial = []
    if a.resume:
        try:
            saved = json.loads(state.read_text(encoding='utf-8'))
            if saved['questions_sha256'] != digest:
                raise ValueError('questions changed; reconcile saved decisions manually before resuming')
            if saved.get('completed'):
                raise ValueError('wizard completed; preserve the profile and gate approvals; archive files manually for a new session')
            if target.exists():
                raise ValueError('profile already exists; refusing to overwrite it')
            questions = {q['id']:q for q in data['questions']}
            ids = [r['id'] for r in saved['answers']]
            if ids != [q['id'] for q in data['questions'][:len(ids)]]:
                raise ValueError('invalid saved answer order')
            initial = [(questions[r['id']],r['decision'],r['source']) for r in saved['answers']]
        except (OSError, ValueError, KeyError, TypeError) as e:
            print('Cannot resume:',e); return 2
    elif state.exists() or target.exists():
        print('Existing wizard progress/profile found. Use --resume for interrupted sessions; archive existing files explicitly to restart.'); return 2

    def save(rows, completed=False):
        state.parent.mkdir(parents=True,exist_ok=True)
        payload={'version':1,'questions_sha256':digest,'completed':completed,
                 'answers':[{'id':q['id'],'decision':d,'source':s,'approval':'Pending'} for q,d,s in rows]}
        temp=state.with_suffix('.tmp')
        temp.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
        temp.replace(state)

    try:
        rows = run(data, use_defaults=a.defaults, initial=initial, save=save)
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended; answered questions saved. Re-run with --resume.")
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x',encoding='utf-8') as f:
        f.write(render_profile(rows))
    save(rows,completed=True)
    print(f"\nwrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
