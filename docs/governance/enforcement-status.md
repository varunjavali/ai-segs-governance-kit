# Enforcement Status (honest ledger)

A rule is called **enforced** only when its technical control is configured **and** verified. Status meanings:

- **Verified (local):** the control exists and was executed in this kit's build environment; self-tests prove it detects violations. It still needs to run in *your* CI to protect *your* repository.
- **Configured, not executed:** the file exists in the kit but could not be run in the build environment (for example a GitHub Actions workflow). Treat as unverified until the first real run is green.
- **Manual activation required:** the control is a repository/platform setting that exists only after someone applies it. Until verified, the rule is not enforced.
- **Checklist only:** no automation; a named owner applies a review checklist.

| Control | Status | How it was verified / what is still needed |
|---|---|---|
| Architecture dependency, public-entry, cycle, unregistered-module, forbidden-import checks (`scripts/check_architecture.py`) | Verified (local) | Regression and valid-input tests with deliberate violations (`tests/governance/test_guardrails.py`); real sample tree passes. Python AST and heuristic JS/TS scanning; exact scope/limits in `docs/architecture/guardrails.md` |
| Secret scan (`scripts/scan_secrets.py`) | Verified (local) | Self-tests detect AWS-key, credential-assignment patterns. Basic regex layer only: add a dedicated scanner (e.g. gitleaks) or platform secret scanning |
| Task prompt validation (`scripts/check_task_prompt.py`) | Verified (local) | Self-tests validate structure and recorded approval metadata, not human identity |
| Feature register validation (`scripts/check_feature_register.py`) | Verified (local) | Self-tests: required canonical table/header, fields, uniqueness, state/approval consistency and evidence |
| PR metadata validation (`scripts/check_pr.py`) | Verified (local logic); CI wiring Configured, not executed | Self-tests on the logic; the `pr-metadata` job has not run on GitHub |
| Docs, links, gate/workflow/environment consistency (`scripts/check_docs.py`) | Verified (local) | Runs in `make verify` |
| Wizard in sync with its source (`scripts/render_wizard.py --check`) | Verified (local) | Runs in `make verify` |
| GitHub Actions `governance.yml` | Configured, not executed | YAML parsed locally; action versions and runners not exercised. Run once on a pull request and confirm job names `governance-checks` and `pr-metadata` appear |
| Dependency review action | Configured, not executed | Needs GitHub plan support for private repositories |
| CODEOWNERS | Manual activation required | Contains `@your-org` placeholders; replace; enable "Require review from Code Owners"; `make setup-check` blocks Gate 4 until replaced |
| Branch protection / required checks / no force-push | Manual activation required | Script `scripts/configure_branch_protection.sh` is syntax-checked and tested with offline mocked API responses (live use needs `gh` CLI and admin rights); run `--apply` then `--verify` and record in the gate log. `release/*` patterns need a ruleset |
| Environment approvals (production reviewers, environment secrets) | Manual activation required | Create GitHub Environments dev, qa, staging, production and add required reviewers |
| Pre-commit hooks | Configured, not executed | Optional local layer; CI is authoritative |
| Lint, type check, unit/integration/e2e, SAST, dependency audit, contract diff, migration validation | Not configured (stack-specific) | Examples in `docs/deployment/stack-examples.md`; choose the stack at Gate 3, configure at Gate 4, then update this row |
| Design-system hardcoded-style lint | Checklist only | Add a stack-specific lint rule, then update this row |
| Review quality, impact analysis completeness, assumption approval | Checklist only | Reviewers and module owners via `docs/governance/skill-guidance.md` and PR template |
| Gate approvals by named humans | Checklist only | `docs/governance/gate-log.md` is a record, not a lock; branch protection plus environment approvals are the technical backing |

Update this table whenever a control is added, changed, or verified; a change from "not executed" to "Verified" needs evidence (CI run link or command output) in the PR.
