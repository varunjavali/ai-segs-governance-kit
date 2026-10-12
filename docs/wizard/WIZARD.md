# Guided Discovery Wizard

> GENERATED from `docs/wizard/questions.json` by `scripts/render_wizard.py`. Do not edit by hand; edit the JSON and re-run the script.

The wizard records proposals for human approval, **one question at a time**. For each question you get: why it matters, the options with trade-offs, a recommended default, and the choice to accept or override it.

How to run it:

- **With Claude (recommended for founders):** paste `prompts/wizard-facilitator-prompt.md` into a chat with this repository attached.
- **In a terminal:** `python scripts/wizard.py` (interactive) or `python scripts/wizard.py --defaults` (writes every recommended default, flagged as an unapproved assumption).

For option questions, type only the option letter. Type `o` to supply an alternative and reason when none fits (for example repository/CLI tooling with no hosted application or database). Alternatives remain proposals pending the responsible human's gate approval.

Progress is atomically saved after each answer to the JSON state under `docs/decisions/`. Run `python scripts/wizard.py --resume` after interruption. A completed profile is written once to `docs/decisions/project-profile.md`; existing state/profile files are never silently overwritten. Archive both explicitly to start a new discovery session, keeping any gate approvals for audit. If questions changed, reconcile saved answers manually before resuming. A choice is only *approved* when the responsible person signs the matching gate in `docs/governance/gate-log.md`. Silent defaults are not approvals.


## Overview: decide now vs. defer

| ID | Topic | Gate | Can defer? |
|---|---|---|---|
| Q01 | 1. Business idea and problem statement | 0 | No - needed before the gate |
| Q02 | 2. Target users, roles, and user journeys | 1 | No - needed before the gate |
| Q03 | 3. Business goals and measurable success criteria | 0 | No - needed before the gate |
| Q04 | 4. Responsive web, mobile, or both | 1 | No - needed before the gate |
| Q05 | 5. Functional requirements and integrations | 1 | No - needed before the gate |
| Q06 | 6. MVP 1, MVP 2, subsequent MVPs, and non-goals | 2 | No - needed before the gate |
| Q07 | 6. MVP 1, MVP 2, subsequent MVPs, and non-goals | 2 | Yes |
| Q08 | 7. Expected users, concurrency, data volume, and growth | 3 | No - needed before the gate |
| Q09 | 8. Availability, reliability, performance, recovery, and security | 3 | No - needed before the gate |
| Q10 | 8. Availability, reliability, performance, recovery, and security | 3 | No - needed before the gate |
| Q11 | 8. Availability, reliability, performance, recovery, and security | 3 | No - needed before the gate |
| Q12 | 9. Architecture style and the explicit microservices decision | 3 | No - needed before the gate |
| Q13 | 10. Technology stack, database, hosting, and infrastructure | 3 | No - needed before the gate |
| Q14 | 10. Technology stack, database, hosting, and infrastructure | 3 | No - needed before the gate |
| Q15 | 11. Budget, timeline, team size, and skill levels | 3 | No - needed before the gate |
| Q16 | 12. Data ownership, API contracts, authentication, and authorization | 3 | No - needed before the gate |
| Q17 | 12. Data ownership, API contracts, authentication, and authorization | 3 | Yes |
| Q18 | 13. Testing and quality strategy | 3 | No - needed before the gate |
| Q19 | 14. Repository setup, branching, ownership, and review policies | 4 | No - needed before the gate |
| Q20 | 14. Repository setup, branching, ownership, and review policies | 4 | No - needed before the gate |
| Q21 | 14. Repository setup, branching, ownership, and review policies | 4 | No - needed before the gate |
| Q22 | 15. CI/CD, environments, deployment, and rollback | 4 | No - needed before the gate |
| Q23 | 15. CI/CD, environments, deployment, and rollback | 4 | Yes |
| Q24 | 16. Monitoring, incident response, cost, sustainability, and maintenance | 3 | Yes |
| Q25 | 16. Monitoring, incident response, cost, sustainability, and maintenance | 3 | Yes |

Questions marked *Yes* may be answered with the default and revisited later; record the deferral so it is a visible assumption, not a silent decision.

## Questions

### Q01 - Topic 1: Business idea and problem statement

**Question:** In two or three sentences: what problem are you solving, and for whom?

**Why it matters:** Every feature must trace back to a real user need. A clear problem statement is the yardstick used later to accept or reject scope.

**Answer format:** free text. Example: *Small clinics lose revenue to missed appointments; we want a booking and reminder tool they can set up in a day.* No default is possible; this must come from you.

**Needed by:** Gate 0. **Can be deferred:** No.

### Q02 - Topic 2: Target users, roles, and user journeys

**Question:** Who are the users and roles (for example customer, staff, admin), and what are the 3-5 most important things each one must be able to do?

**Why it matters:** Roles drive authorization rules, screens, and test scenarios. User journeys become the end-to-end and regression tests that protect working functionality.

**Answer format:** free text. Example: *Patient: find a slot, book, cancel. Receptionist: see the day's schedule, rebook. Admin: manage staff accounts.* No default is possible; this must come from you.

**Needed by:** Gate 1. **Can be deferred:** No.

### Q03 - Topic 3: Business goals and measurable success criteria

**Question:** How will you know the product is succeeding? Give 1-3 measurable goals with a time frame.

**Why it matters:** Measurable goals let the team prioritize and tell the difference between finished and merely busy.

**Answer format:** free text. Example: *30 active clinics within 90 days; no-show rate reduced by 20%.* No default is possible; this must come from you.

**Needed by:** Gate 0. **Can be deferred:** No.

### Q04 - Topic 4: Responsive web, mobile, or both

**Question:** Which platforms must MVP 1 support?

**Why it matters:** Each additional platform multiplies build, test, and release effort. Starting narrow keeps quality high.

| Key | Option | Trade-off |
|---|---|---|
| A | Responsive web only | Fastest and cheapest; one codebase; works on phones through the browser. No app-store presence or deep device features. |
| B | Responsive web + installable PWA | Adds home-screen install and basic offline support at modest cost; limited access to some device features. |
| C | Web + native or cross-platform mobile app | Best device integration and store presence; roughly doubles testing and release work and needs app-store processes. |

**Recommended default:** A - Responsive web only

**Needed by:** Gate 1. **Can be deferred:** No.

### Q05 - Topic 5: Functional requirements and integrations

**Question:** List the functions MVP 1 needs and any external systems it must connect to (payments, email/SMS, maps, identity, accounting, and so on).

**Why it matters:** Integrations are the most common source of hidden effort, cost, security risk, and failure modes.

**Answer format:** free text. Example: *Booking calendar, SMS reminders (provider X), card payments (provider Y).* No default is possible; this must come from you.

**Needed by:** Gate 1. **Can be deferred:** No.

### Q06 - Topic 6: MVP 1, MVP 2, subsequent MVPs, and non-goals

**Question:** Which features are must-haves for MVP 1? Keep it to the smallest set that delivers the core user value.

**Why it matters:** A small MVP ships sooner, gets real feedback sooner, and is easier to build correctly. Anything not listed is out of scope until approved.

**Answer format:** free text. Example: *FEAT-001 book appointment; FEAT-002 cancel appointment; FEAT-003 SMS reminder.* No default is possible; this must come from you.

**Needed by:** Gate 2. **Can be deferred:** No.

### Q07 - Topic 6: MVP 1, MVP 2, subsequent MVPs, and non-goals

**Question:** What is explicitly NOT in MVP 1 (non-goals), and what are the candidates for MVP 2?

**Why it matters:** Writing non-goals down is the cheapest protection against scope creep, including AI-suggested extras.

**Answer format:** free text. Example: *Non-goals: multi-language UI, reporting dashboards. MVP 2 candidates: waiting list, online payments.* No default is possible; this must come from you.

**Needed by:** Gate 2. **Can be deferred:** Yes.

### Q08 - Topic 7: Expected users, concurrency, data volume, and growth

**Question:** How many users do you expect in the first 6-12 months (and at peak at the same time)?

**Why it matters:** Expected load decides whether simple infrastructure is enough and sets the measurable triggers for scaling work.

| Key | Option | Trade-off |
|---|---|---|
| A | Under 100 users; a few concurrent | Single small instance is fine; minimal cost; avoid over-engineering. |
| B | Hundreds to a few thousand users; tens of concurrent | Standard managed hosting with a managed database and basic caching/pagination is sufficient. |
| C | Tens of thousands or more; hundreds+ concurrent | Needs load testing, capacity planning, and possibly queues/caching from the start; higher cost and complexity. |
| D | Unknown | Treated as option B with explicit review triggers (latency, CPU, database load) that prompt re-evaluation. |

**Recommended default:** B - Hundreds to a few thousand users; tens of concurrent

**Needed by:** Gate 3. **Can be deferred:** No.

### Q09 - Topic 8: Availability, reliability, performance, recovery, and security

**Question:** How available must the system be for its most critical workflow?

**Why it matters:** Availability targets drive cost: each extra 'nine' usually means redundancy, more operations work, and stricter release practices.

| Key | Option | Trade-off |
|---|---|---|
| A | Best effort during business hours | Cheapest; acceptable for internal tools and early prototypes. |
| B | 99.5% monthly (about 3.6 hours downtime per month) | Reasonable for most MVPs; needs monitoring, tested rollback, and backups. |
| C | 99.9% monthly (about 43 minutes per month) | Needs redundancy, automated alerts, on-call practice, and zero-downtime deploys. |
| D | 99.95% or higher | Multi-zone design and mature operations; costly. Rarely justified for an MVP. |

**Recommended default:** B - 99.5% monthly (about 3.6 hours downtime per month)

**Needed by:** Gate 3. **Can be deferred:** No.

### Q10 - Topic 8: Availability, reliability, performance, recovery, and security

**Question:** If the system or its data is lost, how much data loss (RPO) and how long an outage (RTO) can the business tolerate?

**Why it matters:** These numbers decide backup frequency, restore drills, and whether replicas are needed.

| Key | Option | Trade-off |
|---|---|---|
| A | RPO 24 hours / RTO 8 hours | Daily backups with a rehearsed restore; low cost. |
| B | RPO 1 hour / RTO 4 hours | Point-in-time recovery and a documented, drilled restore; moderate cost. |
| C | RPO 15 minutes or less / RTO 1 hour or less | Continuous replication and automated failover; high cost and complexity. |

**Recommended default:** A - RPO 24 hours / RTO 8 hours

**Needed by:** Gate 3. **Can be deferred:** No.

### Q11 - Topic 8: Availability, reliability, performance, recovery, and security

**Question:** What is the most sensitive data the product will hold?

**Why it matters:** Data sensitivity sets the security baseline, legal obligations (for example privacy law), encryption, retention, and audit needs.

| Key | Option | Trade-off |
|---|---|---|
| A | No personal data | Lightest security and privacy workload. |
| B | Personal data (names, emails, phone numbers) | Needs data minimization, retention/deletion rules, encryption in transit and at rest, access logging. |
| C | Regulated data (payments, health, children, financial) | Needs formal threat modeling, compliance review, strict access control, audit trails, often a specialist advisor. Prefer certified third parties (e.g. a payment provider) over handling the data yourself. |

**Recommended default:** B - Personal data (names, emails, phone numbers)

**Needed by:** Gate 3. **Can be deferred:** No.

### Q12 - Topic 9: Architecture style and the explicit microservices decision

**Question:** Which architecture style should MVP 1 use? (Explicit microservices decision.)

**Why it matters:** This is the most expensive decision to reverse. Microservices give independent deployment and scaling, but add network failure modes, distributed data consistency, and operational load that small teams often cannot afford at MVP stage.

| Key | Option | Trade-off |
|---|---|---|
| A | Monolith | Simplest to build and run. Risk: boundaries erode over time unless enforced. |
| B | Modular monolith | One deployable with enforced module boundaries and module-owned data. Simple operations now; modules can later be extracted if triggers are met (not effortless). |
| C | Microservices from the beginning | Justified only by independent deployment, separate team ownership, very different scaling profiles, or isolation needs; requires mature operations (observability, CI/CD per service, contract testing). |
| D | Other (explain) | For example serverless or event-driven; needs an ADR justifying it against requirements. |

**Recommended default:** B - Modular monolith

**Needed by:** Gate 3. **Can be deferred:** No.

### Q13 - Topic 10: Technology stack, database, hosting, and infrastructure

**Question:** Which technology stack should the application use?

**Why it matters:** The best stack is usually the one your team and AI assistants can build, test, and operate reliably. Familiarity reduces defects.

| Key | Option | Trade-off |
|---|---|---|
| A | The stack the team already knows best (specify) | Lowest risk and fastest start; confirm it has mature tooling for testing and security. |
| B | TypeScript end-to-end | One language for web and server; large ecosystem; strong AI-assistant support. |
| C | Python backend + TypeScript frontend | Strong for data/ML-heavy products; two toolchains to maintain. |
| D | Other (specify) | Record the reason and the plan to cover tooling gaps. |

**Recommended default:** A - The stack the team already knows best (specify)

**Needed by:** Gate 3. **Can be deferred:** No.

### Q14 - Topic 10: Technology stack, database, hosting, and infrastructure

**Question:** Where will it be hosted, and which database type fits?

**Why it matters:** Hosting choice sets operating effort, cost, and how easily you can scale or recover. Managed services trade some control for far less operations work.

| Key | Option | Trade-off |
|---|---|---|
| A | Managed platform (PaaS) + managed relational database | Least operations effort; automated backups and patches; some vendor lock-in. |
| B | Managed containers on a cloud provider + managed database | More control and portability; more configuration to own. |
| C | Kubernetes | Maximum flexibility; significant expertise and operations cost; rarely justified for an MVP. |
| D | Self-hosted / on-premises | Required by some compliance cases; you own patching, backups, and availability. |

**Recommended default:** A - Managed platform (PaaS) + managed relational database

**Needed by:** Gate 3. **Can be deferred:** No.

### Q15 - Topic 11: Budget, timeline, team size, and skill levels

**Question:** What are your team size, each person's experience level (beginner/intermediate/senior), MVP 1 target date, and monthly infrastructure budget?

**Why it matters:** These constraints shape how much guidance, review, and automation the team needs, and what is realistic to build.

**Answer format:** free text. Example: *6 developers (2 senior, 2 intermediate, 2 beginner); MVP 1 in 12 weeks; infrastructure budget 300 per month.* No default is possible; this must come from you.

**Needed by:** Gate 3. **Can be deferred:** No.

### Q16 - Topic 12: Data ownership, API contracts, authentication, and authorization

**Question:** How will users sign in and how will permissions be controlled?

**Why it matters:** Authentication and authorization are the most security-critical parts of most products and are easy to get subtly wrong.

| Key | Option | Trade-off |
|---|---|---|
| A | Managed identity provider (hosted login, MFA, social login) + role-based access control | Strongest security for the least effort; ongoing per-user cost and vendor dependency. |
| B | Built-in email/password with a vetted framework library | Full control; you own password storage, reset flows, MFA, and abuse protection. |
| C | Enterprise SSO (SAML/OIDC) for business customers | Required by many B2B buyers; more integration and support effort. |
| D | No sign-in (public content only) | Only valid if there is no user-specific data. |

**Recommended default:** A - Managed identity provider (hosted login, MFA, social login) + role-based access control

**Needed by:** Gate 3. **Can be deferred:** No.

### Q17 - Topic 12: Data ownership, API contracts, authentication, and authorization

**Question:** How will API contracts and data ownership be defined?

**Why it matters:** Clear contracts and one owner per dataset are what keep parallel developers and AI agents from breaking each other's work.

| Key | Option | Trade-off |
|---|---|---|
| A | Contract-first (OpenAPI/JSON Schema) and each module owns its tables | Best protection against accidental breaking changes; small up-front effort. |
| B | Code-first with a generated contract, each module owns its tables | Quicker to start; the generated contract must be checked in and diffed in CI. |
| C | Other (specify) | For example GraphQL schema-first or event schemas; record in an ADR. |

**Recommended default:** A - Contract-first (OpenAPI/JSON Schema) and each module owns its tables

**Needed by:** Gate 3. **Can be deferred:** Yes.

### Q18 - Topic 13: Testing and quality strategy

**Question:** How rigorous should testing be for MVP 1?

**Why it matters:** Testing is what stops regressions. Rigor should match the cost of failure.

| Key | Option | Trade-off |
|---|---|---|
| A | Standard: unit + integration + end-to-end for critical journeys, run automatically on every pull request | Recommended baseline for a team using AI assistants. |
| B | Strict: Standard plus contract, load, and security tests before every release | For regulated or high-availability products; slower pipeline and more upkeep. |
| C | Lean: unit tests and a manual smoke test | Only for throwaway prototypes; not recommended for anything customers will rely on. |

**Recommended default:** A - Standard: unit + integration + end-to-end for critical journeys, run automatically on every pull request

**Needed by:** Gate 3. **Can be deferred:** No.

### Q19 - Topic 14: Repository setup, branching, ownership, and review policies

**Question:** Which repository platform will you use?

**Why it matters:** Branch protection, code owners, and CI configuration are platform-specific. The kit's automation targets GitHub.

| Key | Option | Trade-off |
|---|---|---|
| A | GitHub | Kit works as-is (workflows, CODEOWNERS, templates, protection script). |
| B | GitLab / Azure DevOps / Bitbucket | Scripts under scripts/ are portable; CI files, CODEOWNERS format, and protection setup must be translated and re-verified. |

**Recommended default:** A - GitHub

**Needed by:** Gate 4. **Can be deferred:** No.

### Q20 - Topic 14: Repository setup, branching, ownership, and review policies

**Question:** Who is the Technical Owner (architecture and security decisions) and who are the Release Approvers? Name people, and a backup for each.

**Why it matters:** Human accountability requires named people. AI can recommend, but cannot approve its own high-risk decisions or production releases.

**Answer format:** free text. Example: *Technical Owner: Asha (backup Ben). Release Approvers: Asha, Chen.* No default is possible; this must come from you.

**Needed by:** Gate 4. **Can be deferred:** No.

### Q21 - Topic 14: Repository setup, branching, ownership, and review policies

**Question:** What review policy should pull requests follow?

**Why it matters:** Review is the main human control over AI-generated changes.

| Key | Option | Trade-off |
|---|---|---|
| A | 1 approving review + code-owner approval on owned paths | Good balance for up to 10 developers; fast but safe. |
| B | 2 approvals on shared/high-risk paths, 1 elsewhere | Stronger control for shared components, schemas, and security code; slower merges on those paths. |
| C | Pairing/mobbing plus 1 approving review | Best for upskilling beginners; costs developer time. |

**Recommended default:** A - 1 approving review + code-owner approval on owned paths

**Needed by:** Gate 4. **Can be deferred:** No.

### Q22 - Topic 15: CI/CD, environments, deployment, and rollback

**Question:** Which environment flow will you use?

**Why it matters:** Environments let you find problems before customers do. Each extra environment costs money and upkeep.

| Key | Option | Trade-off |
|---|---|---|
| A | Dev -> QA -> Staging -> Production | Recommended standard; one immutable build is promoted through all four. |
| B | Dev -> Staging -> Production (QA folded into Staging) | Cheaper for very small teams; QA and release rehearsal compete for one environment. |

**Recommended default:** A - Dev -> QA -> Staging -> Production

**Needed by:** Gate 4. **Can be deferred:** No.

### Q23 - Topic 15: CI/CD, environments, deployment, and rollback

**Question:** How should deployments be rolled back if something goes wrong?

**Why it matters:** A rehearsed rollback turns an outage into a short incident.

| Key | Option | Trade-off |
|---|---|---|
| A | Redeploy the previous immutable build (database changes must be backward-compatible) | Simple and reliable; requires disciplined migrations. |
| B | Blue/green deployment | Near-instant switch back; doubles production capacity during release. |
| C | Canary/progressive rollout | Limits blast radius; needs strong monitoring. Add only when scale justifies it. |

**Recommended default:** A - Redeploy the previous immutable build (database changes must be backward-compatible)

**Needed by:** Gate 4. **Can be deferred:** Yes.

### Q24 - Topic 16: Monitoring, incident response, cost, sustainability, and maintenance

**Question:** What level of monitoring and incident response do you want at launch?

**Why it matters:** You cannot fix what you cannot see. The baseline is cheap and prevents long undetected outages.

| Key | Option | Trade-off |
|---|---|---|
| A | Baseline: structured logs, uptime check, error tracking, alerts to a named on-call person | Recommended minimum for production. |
| B | Full: baseline plus metrics, tracing, dashboards, and SLO-based alerts | Needed for tight availability targets or microservices; more setup and cost. |
| C | Minimal: uptime check only | Only for internal or pre-launch use. |

**Recommended default:** A - Baseline: structured logs, uptime check, error tracking, alerts to a named on-call person

**Needed by:** Gate 3. **Can be deferred:** Yes.

### Q25 - Topic 16: Monitoring, incident response, cost, sustainability, and maintenance

**Question:** How will you control cost and plan long-term maintenance?

**Why it matters:** Unwatched cloud spend and unmaintained dependencies are common slow-burning failures. Right-sizing also reduces energy use.

| Key | Option | Trade-off |
|---|---|---|
| A | Monthly budget alert and cost review; monthly dependency updates; quarterly technical-debt review | Light routine that prevents surprises. |
| B | Quarterly reviews only | Less effort; slower to catch cost spikes and vulnerable dependencies. |

**Recommended default:** A - Monthly budget alert and cost review; monthly dependency updates; quarterly technical-debt review

**Needed by:** Gate 3. **Can be deferred:** Yes.
