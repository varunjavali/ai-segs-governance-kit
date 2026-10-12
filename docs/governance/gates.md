# Approval Gates

Gates 0-4 occur once per project (and again when scope or architecture changes). Gates 5-6 occur per task. Gates 7-9 occur per release. Gate 10 follows every release. Record every gate in `docs/governance/gate-log.md`. The AI never bypasses a gate because a decision "seems obvious".

| Gate | Name | Exit criteria (evidence required) | Approver | Automation in this kit |
|---|---|---|---|---|
| Gate 0 | Business discovery | Problem statement, goals with measurable success criteria (wizard Q01, Q03) | Founder/product owner | Wizard output |
| Gate 1 | Requirements and user journeys | Roles, journeys, functional requirements, integrations, platforms (Q02, Q04, Q05) | Product owner + Technical Owner | Wizard output |
| Gate 2 | MVP scope and non-goals | MVP 1 feature list in `docs/roadmap/feature-register.md`, non-goals in `docs/roadmap/mvp-roadmap.md` | Product owner | `scripts/check_feature_register.py` |
| Gate 3 | Architecture, stack, quality targets | Architecture style decision (explicit microservices decision), stack, quality attribute plan with owners and verification, ADRs (Q08-Q18, Q24-Q25) | Technical Owner (+ founder for cost/risk) | `scripts/check_docs.py`, ADR template |
| Gate 4 | Repository and workflow initialization | Real owners in CODEOWNERS and `modules.json`; branch protection applied **and verified**; CI green; environments created; `make setup-check` passes | Technical Owner | `make setup-check`, `scripts/configure_branch_protection.sh --verify` |
| Gate 5 | Task readiness | Definition of Ready met; approved seven-block prompt; tier assigned | Per tier (`docs/governance/workflow.md`) | `scripts/check_task_prompt.py`, `scripts/check_pr.py` |
| Gate 6 | Implementation and code review | Diff matches approved scope; tests, checks green; review approved; docs and contracts updated | Reviewer + code owners | CI required checks, CODEOWNERS |
| Gate 7 | QA and release readiness | QA environment verification, regression suite result, security checks, accessibility and performance checks as planned, `docs/deployment/release-checklist.md` section A complete | QA lead + Technical Owner | CI pipeline (stack-specific) |
| Gate 8 | Staging approval | Same artifact verified in Staging: smoke tests, migration rehearsal, rollback rehearsal where relevant | Release Approver | Environment protection (manual) |
| Gate 9 | Production release approval | Release checklist section B complete, rollback plan, on-call named | Release Approver (human; never AI) | GitHub Environment `production` required reviewers (manual setup) |
| Gate 10 | Post-release verification and learning | Post-deploy smoke test, monitoring review, defects and lessons recorded in registers | Technical Owner | Registers in `docs/registers/` |

## Proportionality
Low-risk changes (tier T0/T1) use abbreviated forms but still pass CI. Gates 7-9 for hotfixes follow `docs/operations/runbooks/emergency-hotfix.md` (compressed, never skipped; retrospective review within 2 working days).

## Reopening gates
A change to approved scope, architecture, or quality targets reopens the relevant gate (use `templates/change-request.md`) and invalidates dependent approvals until re-signed.
