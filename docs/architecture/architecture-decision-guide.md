# Architecture and Technology Selection Guide

This guide supports wizard question Q12 (explicit microservices decision) and Gate 3. It neither forces nor forbids microservices: it makes the trade-offs visible and records the decision in an ADR.

## 1. The options in plain language
| | Monolith | Modular monolith | Microservices |
|---|---|---|---|
| What it is | One application, one deployment, one database | One deployment, but code split into modules with enforced boundaries and module-owned data | Many small applications, each deployed and scaled separately, each owning its data |
| Speed to first release | Fastest | Fast | Slowest |
| Operations effort | Lowest | Low | High (networking, observability, per-service pipelines) |
| Failure modes | Few | Few | Many (timeouts, partial failure, retries, distributed data consistency) |
| Team scaling | Hard beyond a few developers without boundaries | Good up to about 10-20 developers | Best for many independent teams |
| Independent deployment / scaling | No | No (whole app) | Yes |
| Boundary discipline | Erodes without enforcement | Static import checks in `scripts/check_architecture.py`; see scanner limits in `docs/architecture/guardrails.md` | Requires configured service access controls and contract checks; network separation alone is insufficient |
| Cost at small scale | Lowest | Low | Highest |

## 2. Decision inputs (score each as Low / Medium / High need, then record in the ADR)
Business domain complexity - expected scale and growth - need for independent deployment - team ownership and size - operational maturity (CI/CD, monitoring, on-call) - security isolation needs - cost constraints - reliability targets - integration requirements - regulatory boundaries.

## 3. Default recommendation
**Modular monolith** for MVP 1 when: one team (or up to about 10 developers), one product, no component needing independent scaling or release cadence, and limited operational maturity. Consider microservices when a material requirement justifies them and the team can operate them. Relevant reasons include: independent deployment is a business requirement; separate teams will own separate parts; scaling or reliability profiles differ sharply; strict isolation (security/compliance) between parts; an existing platform already provides the operational foundations. Record any other style (for example serverless/event-driven) with its justification.

## 4. Rules that apply to every style
1. Define cohesive business modules (`docs/architecture/modules.json`); each has an owner and a purpose.
2. Dependency direction is declared (`allowed_dependencies`) and checked for supported static imports; no circular dependencies; no uncontrolled shared state.
3. Cross-module use goes through a public entry point (interface or API) only.
4. **Data ownership is explicit:** a module's tables are touched only by that module; others use its public interface.
5. Separate business logic from framework and infrastructure details where practical.
6. Stable contracts: APIs and events are versioned and schema-checked (`docs/api/README.md`).
7. Module-level automated tests are possible without starting the whole system.
8. Decisions and the **triggers for revisiting them** are written in ADRs.

## 5. Modular monolith: extraction readiness (honest expectations)
Designing modules so they *can* become services later reduces future cost; it does not make extraction effortless. Before extracting a module, check: it has no direct access to others' tables; all its interactions are through its public interface; it has its own tests; consumers tolerate network latency and failure; there is an owner and an operational plan. Extraction still needs data migration, new deployment pipeline, observability, and failure handling.

**Triggers to revisit the architecture** (set measurable values at Gate 3; examples): a module's deploy frequency or scaling need clearly differs from the rest for three consecutive months; p95 latency or database load of one module exceeds the agreed target after optimization; team grows beyond what shared ownership can coordinate; a compliance boundary requires isolation.

## 6. If microservices are chosen, also define up front
Service ownership - service-owned data (no shared database) - contracts and versioning policy - timeouts, bounded retries with backoff, idempotency keys - circuit breaking/failure isolation - observability (correlated logs, metrics, traces) - independent CI/CD per service - data-consistency approach (sagas/outbox, eventual consistency rules) - local development story - cost estimate. Introduce distributed infrastructure (message brokers, service mesh, Kubernetes) only when a measured need justifies it.

## 7. Technology selection checklist
Team familiarity - mature testing, linting and security tooling - AI-assistant support - hiring pool - hosting fit - license and cost - long-term support - performance fit - exit options. Record the choice and reasons in an ADR (`docs/architecture/adr/0000-template.md`).
