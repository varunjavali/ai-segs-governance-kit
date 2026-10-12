# Testing and Quality Assurance Strategy

Risk-appropriate, not coverage-driven. Prioritize business-critical logic, security-sensitive behavior, data integrity, and high-risk workflows. Coverage percentages are a diagnostic, not proof of quality.

## Test types and when they run
| Test type | Purpose | Local | Pull request | Before release (QA/Staging) | Periodic after deploy |
|---|---|---|---|---|---|
| Static checks (format, lint, types) | Consistency and early errors | Yes | Yes (required) | - | - |
| Governance checks (`make verify`) | Process and architecture guardrails | Yes | Yes (required) | Yes | - |
| Unit | Business rules, edge cases | Yes | Yes (required) | - | - |
| Integration | Module interactions, database, queues | Yes (subset) | Yes (required) | Yes | - |
| API and contract | Compatibility of APIs/events | - | Yes (required if contract touched) | Yes | - |
| Database and migration | Safe, reversible, backward-compatible migrations | - | If migration touched | Yes (on data copy) | - |
| End-to-end (critical journeys) | Journeys from `docs/requirements/` | Optional | Yes (smoke set) | Yes (full set) | Smoke set against production |
| Regression suite | Protect working behavior | - | Affected subset | Full | Nightly in Staging |
| UI / visual / accessibility | Layout, WCAG checks | Optional | Automated a11y on changed screens | Manual keyboard/screen-reader pass on critical journeys | Quarterly |
| Performance and load | Latency, throughput, capacity | - | Budget checks if hot path touched | Yes when planned | Quarterly or before expected spikes |
| Security | Dependency audit, SAST, secrets, authz tests | Secrets (pre-commit) | Yes (required) | DAST/penetration check when risk warrants | Dependency scans continuous |
| Resilience and recovery | Failure injection, restore drill | - | - | Before first launch and major changes | Backup restore drill quarterly |

Specify the concrete tool and command for each row at Gate 3/4 in `docs/deployment/stack-examples.md`; unfilled rows are visible gaps, not silent omissions.

## Rules
1. Every behavior change has a test; every bug fix has a regression test that failed before the fix.
2. **Never delete, skip, or weaken a failing test to pass a build.** A test may be changed only with reviewer approval and a written reason.
3. Flaky tests are defects: log in `docs/registers/defect-log.md`, quarantine with an owner and deadline (max 14 days), never ignore.
4. Tests assert observable behavior (acceptance criteria), not implementation details.
5. Critical journeys list lives in `docs/requirements/README.md`; each has an end-to-end test; the feature register's "Test requirements" column links tests.
6. Test data contains no real personal data.
7. AI-written tests are reviewed with extra care: confirm they would fail if the behavior were broken.
