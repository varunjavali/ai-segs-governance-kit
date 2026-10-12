# Git, Branching, and Environment Governance

Environment flow: **Dev -> QA -> Staging -> Production**. One immutable build artifact is promoted through all four; configuration and secrets differ per environment, the artifact does not.

## Branch model (default)
| Branch | Purpose | Protection | Deploys to |
|---|---|---|---|
| `feature/*`, `fix/*`, `chore/*` | Short-lived work, one task each | None; must open a PR | - |
| `main` | Integration; always releasable | PR required, required checks, code-owner review, up-to-date, no force-push, linear history | Dev (automatic) |
| `release/x.y` | Release candidate cut from `main` | Same as `main`; only fixes cherry-picked or merged via PR | QA, then Staging (same build) |
| Tag `vX.Y.Z` | Immutable release marker | Tag creation limited to Release Approvers | Production (manual approval) |
| `hotfix/*` | Emergency fix from the production tag | PR to `release/x.y` and `main` | per `docs/operations/runbooks/emergency-hotfix.md` |

Teams preferring branch-per-environment (`develop`, `qa`, `staging`, `main`) may use it; record the choice in an ADR and keep the same protections. **Branch names are labels, not controls:** the real controls are the settings below.

## Controls that must exist (and be verified, see `docs/governance/enforcement-status.md`)
1. Branch protection (or rulesets) on `main` and `release/*`: required PR, required status checks `governance-checks` and `pr-metadata`, code-owner review, dismiss stale approvals, conversation resolution, no force push, no deletion, applies to admins. Apply with `scripts/configure_branch_protection.sh`; for `release/*` patterns use a repository ruleset with the same settings.
2. `.github/CODEOWNERS` with real owners; protected paths below require Technical Owner review.
3. GitHub Environments `dev`, `qa`, `staging`, `production`: environment-scoped secrets; required reviewers on `staging` and `production`; deployment branches limited to `main`/`release/*`/tags.
4. Versioned builds: artifact named with version and commit SHA; promotion never rebuilds.
5. Controlled database migrations: forward migrations reviewed, validated on a copy of data in QA/Staging, backward-compatible with the previous release so rollback works.
6. Release approval, smoke tests, and rollback procedure (`docs/deployment/release-checklist.md`).

## Protected paths (Technical Owner review)
`docs/architecture/modules.json`, `docs/architecture/adr/`, `.github/`, `scripts/`, `AGENTS.md`, `CLAUDE.md`, `docs/governance/`, database migration directories, infrastructure configuration, authentication/authorization code.

## Commit and PR rules
Conventional, focused commits; PR template filled completely; PR references FEAT/BUG/CHG/TASK/DEBT id; AI-assisted work states so and includes the handoff report.

Default environment sequence is Dev -> QA -> Staging -> Production. Wizard Q22 option B is a proposal requiring a documented approval/ADR and synchronized release/gate/pipeline documentation before use. Branch-protection --verify checks the requested legacy settings; separately audit rulesets, bypass actors and tag protections in your provider.
