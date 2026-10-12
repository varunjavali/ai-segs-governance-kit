# Project Profile (wizard output)

> Written by `scripts/wizard.py`. Entries are **proposals** until the responsible approver signs the matching gate in `docs/governance/gate-log.md`.

| ID | Gate | Decision | Source | Gate approval |
|---|---|---|---|---|
| Q01 | 0 | Small software teams using AI coding assistants struggle with inconsistent code, unclear requirements, regressions, and conflicting changes. We want a guided governance toolkit that helps founders and developers plan, review, test, and release software with clear ownership and approval gates. | chosen | Pending |
| Q02 | 1 | Founder/product owner: define goals, prioritize MVP features, clarify requirements, approve scope. Developer: read approved tasks, implement changes, run tests, submit PRs. Reviewer/module owner: approve task readiness, review changes, verify evidence, protect module boundaries. Technical Owner: approve architecture, define quality targets, resolve conflicts, oversee safeguards. Release Approver/operations owner: assess release readiness, approve releases, monitor service health, coordinate rollback. | chosen | Pending |
| Q03 | 0 | Within 30 days, all active developers use the approved task workflow and PR checklist. Within 60 days, every PR runs governance checks and application tests, with required human reviews before merging. Within 90 days, reduce regression defects found after merging by 30% compared with the first 30-day baseline. | chosen | Pending |
| Q04 | 1 | A - Responsive web only | chosen | Pending |
| Q05 | 1 | MVP 1 needs guided project discovery with save/resume, requirements and feature tracking, seven-block task templates, architecture checks, PR metadata validation, human approval records, verification reports, and installation guidance. Git integration supplies changed-file evidence; GitHub integration provides CI checks and branch protection after authorized setup. No payments, email/SMS, external identity provider, or production deployment automation is required for MVP 1. | chosen | Pending |
| Q06 | 2 | FEAT-001 guided project discovery with save/resume; FEAT-002 requirements, MVP scope, and feature register validation; FEAT-003 seven-block task templates and approval metadata checks; FEAT-004 architecture boundary checks; FEAT-005 PR validation using actual changed files and verification evidence; FEAT-006 local verification and GitHub CI configuration; FEAT-007 branch-protection setup and verification guidance. | chosen | Pending |
| Q07 | 2 | MVP 1 non-goals: web dashboard, mobile app, payments, email/SMS notifications, external identity integration, automatic human approvals, live repository changes without authorization, and production deployment automation. MVP 2 candidates: a read-only governance dashboard, traceability reports linking requirements to PRs and test results, and adapters for additional repository platforms. Candidates remain unapproved until assessed and prioritized. | chosen | Pending |
| Q08 | 3 | A - Under 100 users; a few concurrent | chosen | Pending |
| Q09 | 3 | A - Best effort during business hours | chosen | Pending |
| Q10 | 3 | A - RPO 24 hours / RTO 8 hours | chosen | Pending |
| Q11 | 3 | B - Personal data (names, emails, phone numbers) | chosen | Pending |
| Q12 | 3 | D - Other (explain): Repository-based toolkit with modular Python CLI scripts and GitHub Actions configuration. No hosted application, database, or distributed services in MVP 1. | chosen | Pending |
| Q13 | 3 | D - Other (specify): Python 3.12+ for governance CLI scripts, Git for version control, Bash for verification scripts, and GitHub Actions for CI. No application frontend, backend server, or database in MVP 1. TypeScript sample modules are demonstrations only. | chosen | Pending |
| Q14 | 3 | Other: GitHub repository and GitHub Actions, with local CLI execution. No application hosting or database is needed for MVP 1. | chosen-other | Pending |
| Q15 | 3 | Team: [number] developers — [number] beginner, [number] intermediate, [number] senior. MVP 1 target: [date]. Monthly infrastructure budget: [amount and currency], covering repository/CI usage and backups. | chosen | Pending |
| Q16 | 3 | Other: Use GitHub accounts for repository access, with MFA, team permissions, CODEOWNERS, and required human reviews. Local CLI access follows operating-system permissions. No separate application login in MVP 1. | chosen-other | Pending |
| Q17 | 3 | C - Other (specify): No application API or database in MVP 1. Define CLI arguments, exit codes, configuration formats, and saved wizard-state format as documented interfaces. Keep each governance record in one canonical file with a named owner; changes to these interfaces require review and compatibility checks. | chosen | Pending |
| Q18 | 3 | Other: Run validator unit/regression tests, CLI integration tests, and complete wizard save/resume journeys on every PR. Include valid-input cases, malformed-input rejection, mocked GitHub responses, documentation/configuration checks, shell checks, and ZIP extraction verification before release. Governance tests do not prove application behavior or production readiness. | chosen-other | Pending |
| Q19 | 4 | A - GitHub | chosen | Pending |
| Q20 | 4 | Technical Owner: [varun]; backup: [varun]. Release Approver: [varun]; backup: [varun]. | chosen | Pending |
| Q21 | 4 | A - 1 approving review + code-owner approval on owned paths | chosen | Pending |
| Q22 | 4 | Other: Local development -> PR CI verification -> fresh ZIP extraction and smoke tests -> versioned kit release. MVP 1 has no deployed application environments. Any future hosted application needs its own approved environment and promotion plan. | chosen-other | Pending |
| Q23 | 4 | Other: Restore the previous versioned kit ZIP or Git release tag and rerun verification. Back up project records and wizard progress before upgrading; preserve them during rollback and check format compatibility. No application deployment or database rollback in MVP 1. | chosen-other | Pending |
| Q24 | 3 | Other: Monitor CI failures, failed or interrupted CLI runs, security findings, and repository/CI costs. Retain verification reports and assign a maintainer to triage issues and coordinate fixes or rollback. No hosted-service uptime monitoring in MVP 1. | chosen-other | Pending |
| Q25 | 3 | A - Monthly budget alert and cost review; monthly dependency updates; quarterly technical-debt review | chosen | Pending |

## Assumptions and open items

Each item below is an assumption or gap, not an approved decision. Resolve it at the gate shown.

- None
