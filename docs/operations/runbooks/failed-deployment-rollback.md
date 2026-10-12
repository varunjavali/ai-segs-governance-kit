# Runbook: Failed deployment and rollback

- Last rehearsed: never (update after the first drill)
- Owner: Operations owner (see `docs/team/roles-and-ownership.md`)

## Trigger
Post-deploy smoke test fails, error rate or latency jumps after a release, or a critical defect is found in production.

## Severity
Treat as SEV2 unless users cannot complete a critical workflow (then SEV1).

## Immediate actions
1. Pause further deployments. 2. Decide: rollback vs forward fix (rollback unless the change included an irreversible data change). 3. Release Approver or Incident Lead authorizes.

## Diagnosis
Compare the release diff and migration list; check whether the new migration is backward-compatible with the previous artifact.

## Recovery
Rollback: redeploy the previous immutable artifact version recorded in the release checklist; confirm configuration matches. If a migration ran, confirm the old version works with the new schema; if not, use forward recovery (fix + redeploy) or restore per `backup-restore.md`. Never rebuild the old version; redeploy the stored artifact.

## Communication
Notify stakeholders of rollback and impact; update the release record.

## Verification
Smoke tests pass on the previous version; metrics normal; the failed version is blocked from promotion until fixed and re-verified in QA and Staging.

## Follow-up
Blameless review within 5 working days (`templates/incident-postmortem.md`); update `docs/registers/defect-log.md` and `docs/registers/improvement-register.md`; prefer a new automated check over a reminder.
