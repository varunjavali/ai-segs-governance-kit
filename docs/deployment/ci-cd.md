# CI/CD

## What exists in this kit
`.github/workflows/governance.yml` runs on every pull request and on pushes to `main`/`release/**`:
- `governance-checks` - `scripts/verify_all.sh` (docs, wizard sync, feature register, task prompts, architecture guardrail, secret scan, shell syntax, guardrail self-tests)
- `pr-metadata` - `scripts/check_pr.py` (canonical task/feature approval metadata, complete sections/checklist, meaningful N/A reasons, command evidence and actual changed paths; see `docs/architecture/guardrails.md`)
- `dependency-review` - dependency changes vulnerability review (requires GitHub support for the repository plan)

Make `governance-checks` and `pr-metadata` **required status checks** via branch protection (`scripts/configure_branch_protection.sh`).

## What you add at Gate 4 (stack-specific, see `docs/deployment/stack-examples.md`)
Build, lint, type check, unit/integration/contract tests, dependency audit, SAST, database migration validation, artifact build with version and commit SHA, smoke tests.

## Pipeline stages
| Stage | Trigger | Content | Environment | Gate |
|---|---|---|---|---|
| Validate | Every PR | Governance + stack checks + tests | none | 6 |
| Integrate | Merge to `main` | Build immutable artifact (`app-<version>-<sha>`), deploy | Dev | - |
| Release candidate | Cut `release/x.y` | Promote same artifact; full regression, security, accessibility, performance as planned | QA | 7 |
| Rehearse | After QA green | Promote; migration and rollback rehearsal; smoke | Staging | 8 |
| Release | Tag `vX.Y.Z` + approval | Promote same artifact; post-deploy smoke; monitor | Production | 9, 10 |

## Rollout and recovery
Default: redeploy the previous immutable build (wizard Q23 = A); migrations are backward-compatible so rollback is safe. Prefer **forward recovery** (fix and redeploy) when rollback would lose data. Blue/green and canary only when scale and monitoring justify the complexity. Procedures: `docs/operations/runbooks/failed-deployment-rollback.md`.

## Pipeline security
Workflow `permissions` default to read-only; secrets via environment scopes; third-party actions currently use version tags, not immutable SHA pins. Pin reviewed commits during adoption. No production job is included; an installed production job must require environment approval.
