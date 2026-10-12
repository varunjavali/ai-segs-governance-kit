# Runbook: Performance degradation

- Last rehearsed: never (update after the first drill)
- Owner: Operations owner (see `docs/team/roles-and-ownership.md`)

## Trigger
Latency SLO breach, saturation alerts, or user reports of slowness.

## Severity
SEV2 by default; SEV1 if critical workflow effectively unavailable.

## Immediate actions
1. Check for a recent deploy and roll back if correlated. 2. Protect capacity: rate limits, disable non-critical background work, scale out if safe.

## Diagnosis
Look at the golden signals: latency, traffic, errors, saturation. Database: slow query log, locks, connection pool, missing indexes. Payload sizes, cache hit rate, third-party latency. Profile before changing code.

## Recovery
Apply the targeted fix (index, query change, cache, timeout tuning); load-test the fix in Staging when time allows; capacity change if the cause is growth (record the architecture-evolution trigger).

## Communication
Tell stakeholders expected impact and ETA.

## Verification
Latency and error rate within SLO for 30 minutes; add or adjust a performance budget check so the regression is caught earlier.

## Follow-up
Blameless review within 5 working days (`templates/incident-postmortem.md`); update `docs/registers/defect-log.md` and `docs/registers/improvement-register.md`; prefer a new automated check over a reminder.
