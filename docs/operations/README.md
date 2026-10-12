# Operations

Runbooks live in `docs/operations/runbooks/`. Each follows `templates/runbook.md`: trigger, severity, immediate actions, diagnosis, recovery, communication, verification, follow-up.

| Runbook | Use when |
|---|---|
| `runbooks/incident-response.md` | Any production incident (start here) |
| `runbooks/failed-deployment-rollback.md` | A release misbehaves |
| `runbooks/backup-restore.md` | Data loss/corruption; also the quarterly drill |
| `runbooks/performance-degradation.md` | Slow responses or saturation |
| `runbooks/security-incident.md` | Suspected breach or leaked secret |
| `runbooks/dependency-failure.md` | A third-party service or library fails |
| `runbooks/emergency-hotfix.md` | Urgent production fix that cannot wait for the normal flow |

Runbooks are drafts until rehearsed. Record each rehearsal date in the runbook header; an unrehearsed runbook is a risk item in `docs/registers/risk-log.md`.
