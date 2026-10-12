# Runbook: Backup restoration (and quarterly drill)

- Last rehearsed: never (update after the first drill)
- Owner: Operations owner (see `docs/team/roles-and-ownership.md`)

## Trigger
Data loss or corruption; or the scheduled quarterly restore drill.

## Severity
SEV1 for production data loss; drill is planned work.

## Immediate actions
1. Stop writes that could worsen corruption (maintenance mode). 2. Identify the last known good point in time. 3. Get Technical Owner approval for production restore.

## Diagnosis
Determine scope: which tables/tenants, since when, cause (bug, human error, attack). Check backup catalog and that the target recovery point meets the agreed RPO.

## Recovery
Restore into a separate environment first; verify integrity and row counts; then promote or copy back affected data. Record achieved RPO and RTO versus the targets in the quality attribute plan.

## Communication
Inform affected users if data was lost; document the data gap.

## Verification
Application integrity checks and critical-journey tests pass on restored data; reconcile with logs. For drills: record date, duration, issues; fix gaps within 14 days.

## Follow-up
Blameless review within 5 working days (`templates/incident-postmortem.md`); update `docs/registers/defect-log.md` and `docs/registers/improvement-register.md`; prefer a new automated check over a reminder.
