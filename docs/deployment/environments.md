# Environments

Flow: **Dev -> QA -> Staging -> Production**. The same immutable artifact moves through all four; only configuration and secrets change. (If wizard Q22 chose option B, QA is folded into Staging; update this file and `docs/governance/git-environment-governance.md` together.)

| Environment | Purpose | Deploys | Data | Access | Approval to deploy |
|---|---|---|---|---|---|
| Dev | Integration of merged work; fast feedback | Automatic on merge to `main` | Synthetic | Developers | None |
| QA | Release-candidate verification (Gate 7) | Automatic when a `release/x.y` branch is cut | Synthetic, realistic volume | Developers, QA | None (checks must pass) |
| Staging | Production-like rehearsal: migrations, performance, rollback (Gate 8) | Same build promoted from QA | Anonymized copy or synthetic at production scale; never raw personal data | Limited | Release Approver |
| Production | Real users (Gate 9) | Same build promoted from Staging | Real | Minimal; audited | Release Approver (human) |

Rules: environment-specific secrets stored per environment; no direct production changes outside the pipeline (emergency path: `docs/operations/runbooks/emergency-hotfix.md`); infrastructure defined as code where infrastructure exists; Dev/QA scaled down or stopped when idle to save cost.
