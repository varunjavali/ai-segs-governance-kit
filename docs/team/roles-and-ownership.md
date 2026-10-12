# Roles and Ownership

Fill names at Gate 4 (wizard Q20). Every role has a named backup. AI agents hold no roles with approval authority.

| Role | Responsibilities | Name | Backup |
|---|---|---|---|
| Founder / Product owner | Business goals, scope approval (Gates 0-2), priorities | | |
| **Technical Owner** | Architecture, security, ADRs, exceptions, T3 approvals, guardrail config, escalations | | |
| Release Approver(s) | Gates 8-9, production releases, hotfix approval | | |
| QA lead | Test strategy, regression suite health, Gate 7 | | |
| Security owner | Security baseline, dependency/secret findings, incident lead for security | | |
| Design-system owner | Tokens, shared components | | |
| Operations owner | CI/CD, environments, monitoring, runbooks, cost | | |
| Module owners | One per module in `docs/architecture/modules.json`: module design, PR review, Gate 5 for T1/T2 | | |
| Developers | Implement tasks via the standard workflow | | |
| Reviewers | Review per `docs/governance/skill-guidance.md` | | |

## Rules
- Technical Owner reviews architecture-significant changes only; not every trivial change.
- Roles may be combined in a small team, but nobody approves their own production release or exception.
- `.github/CODEOWNERS` mirrors this table for paths and modules.
