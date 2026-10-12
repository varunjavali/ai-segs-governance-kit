# Runbook: Incident response (start here)

- Last rehearsed: never (update after the first drill)
- Owner: Operations owner (see `docs/team/roles-and-ownership.md`)

## Trigger
Alert fires, user reports, or monitoring shows breach of an SLO for a critical workflow.

## Severity
SEV1: critical workflow down or data/security at risk. SEV2: major degradation. SEV3: minor, workaround exists.

## Immediate actions
1. Name an Incident Lead (one person decides). 2. Open an incident channel and a timeline note. 3. Stop the bleeding first: roll back the last change, disable the feature flag, or shed load. 4. Assign a communicator.

## Diagnosis
Check, in order: what changed recently (deploys, config, migrations, dependencies)? Dashboards: error rate, latency, saturation. Logs filtered by correlation id. Third-party status pages. Recent alerts.

## Recovery
Apply the smallest safe fix: rollback (`failed-deployment-rollback.md`), restore (`backup-restore.md`), dependency workaround (`dependency-failure.md`), or forward fix via hotfix flow (`emergency-hotfix.md`). Do not experiment on production without the Incident Lead's approval.

## Communication
SEV1: update stakeholders every 30 minutes; SEV2: every 60 minutes; final summary when resolved. State facts, impact, next update time.

## Verification
Critical-journey smoke test passes; error rate and latency back within SLO for 30 minutes; alerts cleared.

## Follow-up
Blameless review within 5 working days (`templates/incident-postmortem.md`); update `docs/registers/defect-log.md` and `docs/registers/improvement-register.md`; prefer a new automated check over a reminder.
