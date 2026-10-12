# Automated Architecture Guardrails

Status values are defined precisely in `docs/governance/enforcement-status.md`. A rule is only called **enforced** when the technical control is configured *and* verified. Everything else has a named owner and a review checklist.

| Guardrail | Catches | Implementation | Owner |
|---|---|---|---|
| Module dependency direction | A module importing one it may not depend on | `scripts/check_architecture.py` + `docs/architecture/modules.json` (runs in CI via `verify_all.sh`) | Technical Owner |
| Public entry point only | Deep imports into another module's internals | same script | Technical Owner |
| Circular dependencies | Cycles between modules (configured and observed) | same script | Technical Owner |
| Unregistered modules | New module directories added without an ADR | same script | Technical Owner |
| Forbidden imports | Framework/infrastructure leaking into core modules | `forbidden_imports` rules in `modules.json` | Technical Owner |
| Secret detection | Credentials in commits | `scripts/scan_secrets.py` (basic) - add gitleaks or platform secret scanning (stack decision) | Security owner |
| Scope traceability | PRs with no approved work item | `scripts/check_pr.py` in `pr-metadata` job | Reviewers |
| Scope governance | Unapproved features in the register | `scripts/check_feature_register.py` | Product owner |
| Task readiness | Unapproved/incomplete prompts | `scripts/check_task_prompt.py` | Module owners |
| Docs and rule consistency | Broken links, missing gates/steps, drifted wizard | `scripts/check_docs.py`, `scripts/render_wizard.py --check` | Technical Owner |
| Protected files / code ownership | Unreviewed edits to architecture, CI, scripts | `.github/CODEOWNERS` + branch protection (manual activation) | Technical Owner |
| Required PR checks and review | Merging unreviewed or red code | Branch protection via `scripts/configure_branch_protection.sh` (manual activation) | Technical Owner |
| Formatting, linting, type checks | Style and type errors | Stack-specific, see `docs/deployment/stack-examples.md` | Module owners |
| Dependency vulnerability scanning | Known-vulnerable packages | `dependabot.yml` + `actions/dependency-review-action` in CI (plan-dependent) + stack audit command | Security owner |
| API/schema compatibility | Breaking contract changes | Stack-specific contract diff (e.g. OpenAPI diff) - example in `docs/deployment/stack-examples.md` | API owners |
| Database migration validation | Unsafe or irreversible migrations | Run migrations on a data copy in QA/Staging; checklist in `docs/deployment/release-checklist.md` | Data owner |
| Design-system conventions | Hardcoded colors/spacing, duplicate components | Stack-specific lint rule + review checklist in `docs/design-system/design-system-governance.md` | Design-system owner |
| Deployment permissions | Unapproved production deploys | GitHub Environment required reviewers (manual activation) | Release Approver |

## Where a rule cannot be automated
Use the review checklist in the relevant doc and name the owner in the table above. Do not describe such a rule as enforced.

## Scanner and metadata boundaries
Python files use the standard-library AST: every import alias is visited, including nested and multiline imports. From-list aliases are resolved to on-disk .py modules/packages to distinguish an imported submodule from a public symbol. Public root symbols, configured entry files and public directories remain valid. Dynamic imports, runtime re-exports, monkey patches, module-level __getattr__, installed package layouts and data access are not analyzed. Add native dependency tooling and application tests for the chosen stack.

JS/TS scanning is a regular-expression heuristic for quoted import/export-from, require() and import() specifiers. It is not a parser: comments/strings may cause false positives; unusual whitespace/comments, escapes, template literals, computed specifiers, import-equals and alternative alias mappings may be missed. Literal import() paths can be scanned; computed dynamic imports cannot. It does not validate symbol exports or runtime dependencies.

Missing source_root always fails. Zero supported files are allowed only when the source directory exists and modules.json explicitly has allow_empty_bootstrap set to true, before application implementation; it is absent/disabled in this kit. This opt-in does not suppress configuration or module registration errors.

PR validation requires the sections and labeled checks in the PR template. Scope, Register, Governance, Integrity and Architecture cannot be N/A; other checks need a meaningful reason when inapplicable. Verification groups contain Command, Exit-code and Outcome with substantive content and successful exit codes. This validates claims, not test execution; CI results and reviewers verify the claims. Do not submit incomplete template text.

All nontrivial work IDs resolve to exactly one saved seven-block prompt in prompts/tasks with valid named approval metadata and tier. FEAT IDs also resolve to an approved, active feature register row with evidence. Other work IDs use their task prompt as the canonical approval record; link applicable defect/change/debt records from that prompt. Example prompts are never approval records. Provider-authenticated reviews and the gate owner's identity remain manual/installed controls.

Local PR command: `python scripts/check_pr.py --body-file pr-body.txt --changed-files changed-files.json`. The JSON must be an array of repository-relative paths from the actual diff (include both sides of renames). In CI, full base/head commit SHAs are supplied as environment variables and git computes the changed paths. Never accept an author-curated path list as authoritative CI evidence. Trivial eligibility is a conservative Markdown path allowlist in the validator; reviewers still confirm that the diff is wording-only. Application, security, architecture, CI, migration, scripts and governed policy changes require normal controls. Changes to the validator or workflow themselves require trusted owner review; a green check from editable PR code is not tamper-proof authorization.

The branch-protection policy is defined once in `scripts/check_branch_protection.py`; the shell script uses it for both PUT and structured GET validation. All requested fields, including both checks, review count, strictness and deletion/force-push prevention, are compared. Extra checks are permitted. Local mock tests do not verify provider enforcement, bypass actors, rulesets, environment approvals or denied operations on a live repository.
