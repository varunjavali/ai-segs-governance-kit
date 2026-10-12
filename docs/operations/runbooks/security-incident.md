# Runbook: Security incident

- Last rehearsed: never (update after the first drill)
- Owner: Operations owner (see `docs/team/roles-and-ownership.md`)

## Trigger
Suspected breach, leaked secret, unexpected access, vulnerability exploited, or malware alert.

## Severity
Treat as SEV1 until scoped.

## Immediate actions
1. Notify the Technical Owner/security owner immediately. 2. Contain: revoke and rotate exposed credentials, disable affected accounts or features, preserve logs and evidence (do not delete). 3. Do not discuss publicly until the owner approves.

## Diagnosis
Determine what was accessed, since when, how. Review audit logs, access logs, recent commits and deployments. A secret in git history counts as compromised even if the commit was removed.

## Recovery
Remove the access path; patch or rotate; redeploy through the normal pipeline (hotfix flow if urgent); restore from clean backups if integrity is in doubt.

## Communication
Legal/regulatory notification obligations are decided by the founder with advice (personal-data breaches often have strict deadlines). Inform affected users as advised.

## Verification
Confirm no further unauthorized activity; secrets rotated everywhere; add detection (scan rule, alert) and a regression test; complete the post-mortem.

## Follow-up
Blameless review within 5 working days (`templates/incident-postmortem.md`); update `docs/registers/defect-log.md` and `docs/registers/improvement-register.md`; prefer a new automated check over a reminder.
