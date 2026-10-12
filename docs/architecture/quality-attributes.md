# Quality Attribute Plan

Each project approves its own plan at **Gate 3**. The "starting point" values are suggestions to discuss, not mandatory thresholds; do not impose identical numbers on every application. Fill the plan table with approved targets, owners, and verification, and keep it current.

## Plan table (copy per project; one row per attribute you commit to)
| Attribute | Measurable target (approved) | Assumptions and trade-offs | Owner | Verification method | Cadence |
|---|---|---|---|---|---|
| | | | | | |

## Guidance by area (what to consider, suggested starting points, how to verify)

### Reliability
- Define SLIs/SLOs for each critical workflow (e.g. success rate of "book appointment"). Starting point: 99.5% monthly for MVPs (wizard Q09).
- Failure-mode analysis for each integration; graceful error handling; timeouts on every outbound call; bounded retries with backoff; idempotency for retried writes.
- Health checks (liveness and readiness); dependency-failure behavior defined (degrade, queue, or fail clearly).
- Database integrity: constraints, transactions, safe migrations. Backups with **restore tested** (RPO/RTO from Q10).
- Verify: failure-injection tests for critical paths, restore drill each quarter, incident runbooks rehearsed.

### Scalability and elasticity
- State expected concurrency and data volume (Q08); stateless application instances where practical.
- Indexes for known queries, connection pooling, pagination and bounded queries, caching with invalidation rules, background jobs/queues only when justified, backpressure.
- Verify: load test against agreed peak before each release that changes hot paths; capacity review quarterly; documented triggers for architecture evolution.

### Operational excellence
- Reproducible builds and environments; infrastructure as code where infrastructure exists; configuration and secrets outside code.
- CI/CD, structured logs, metrics, traces (as justified), dashboards, actionable alerts (each alert has a runbook); release and rollback procedures; routine backup verification.
- Verify: new engineer can build and deploy from README in under a day; alert-to-runbook mapping reviewed quarterly.

### Performance efficiency
- Targets per critical flow, e.g. p95 API latency and page load budget on a mid-range phone and slow network.
- Query and payload optimization; efficient frontend assets; profiling before optimizing.
- Verify: performance checks in CI for budgets that matter; regression comparison before release.

### Sustainability and resource efficiency
- Right-size infrastructure; scale down non-production when idle; no permanently running resources without an owner; efficient storage, retention, and network use; caching where it reduces waste.
- Accessibility and efficiency on low-powered devices and slow networks.
- Verify: monthly cost and utilization review; delete-by-date tags on temporary resources.

### Security and privacy
- Threat model appropriate to risk (`templates/threat-model.md`); authentication, authorization with least privilege, secure defaults; input validation; secure session handling; safe error messages.
- Encryption in transit and at rest; secrets management; dependency scanning; data minimization, retention and deletion rules, audit logs where required.
- Verify: see `docs/security/security-baseline.md`.

### Maintainability, interoperability, accessibility
- Cohesive modules, clear interfaces, conventions, useful tests; versioned API/event contracts; data integrity checks.
- Semantic HTML, keyboard navigation, color contrast, screen-reader labels, responsive layouts (target: WCAG 2.2 AA unless decided otherwise).
- Verify: lint/type checks, contract diff checks, automated accessibility checks in CI plus manual keyboard/screen-reader check for critical journeys.
