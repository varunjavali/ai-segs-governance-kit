# Runbook: Dependency failure (third-party service or library)

- Last rehearsed: never (update after the first drill)
- Owner: Operations owner (see `docs/team/roles-and-ownership.md`)

## Trigger
Provider outage, API errors/timeouts from an integration, or a critical vulnerability/breakage in a library.

## Severity
SEV2 by default; SEV1 if a critical workflow depends on it with no fallback.

## Immediate actions
1. Confirm via the provider status page and own metrics. 2. Enable the degraded mode (queue requests, show clear error, use cached data) defined for that integration. 3. Stop retries from amplifying load (bounded retries, backoff, circuit breaker).

## Diagnosis
Check timeouts, error codes, recent changes on our side, version upgrades, credentials expiry.

## Recovery
Wait/degrade for provider outages; for libraries pin to the last good version or apply the patched version through the normal pipeline; replay queued work idempotently after recovery.

## Communication
Tell users about degraded functionality and expected recovery.

## Verification
Queued work drained without duplicates; integration health check green; update the integration's failure-mode notes.

## Follow-up
Blameless review within 5 working days (`templates/incident-postmortem.md`); update `docs/registers/defect-log.md` and `docs/registers/improvement-register.md`; prefer a new automated check over a reminder.
