# Runbook: Emergency hotfix procedure

- Last rehearsed: never (update after the first drill)
- Owner: Operations owner (see `docs/team/roles-and-ownership.md`)

## Trigger
A production defect or vulnerability with serious user, data, or security impact that cannot wait for the normal release.

## Severity
SEV1 or SEV2 confirmed by the Incident Lead.

## Immediate actions
1. Incident Lead and Release Approver agree a hotfix is needed (consider rollback first). 2. Branch `hotfix/<id>` from the production tag.

## Diagnosis
Reproduce; write the failing regression test first.

## Recovery
Smallest possible fix; full CI must pass (no bypass); one reviewer who is not the author, plus Technical Owner for T3 changes; build once; deploy to Staging for a smoke test if time permits; Release Approver approves production deploy; then merge the fix to `release/x.y` and `main` through PRs so it is not lost.

## Communication
Stakeholders informed at start and end; record in the incident timeline.

## Verification
Production smoke test; monitoring review for 1 hour; retrospective review of the hotfix within 2 working days, including any compressed gates, logged in `docs/governance/gate-log.md`.

## Follow-up
Blameless review within 5 working days (`templates/incident-postmortem.md`); update `docs/registers/defect-log.md` and `docs/registers/improvement-register.md`; prefer a new automated check over a reminder.
