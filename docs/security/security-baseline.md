# Security and Privacy Baseline

Scaled to the data sensitivity chosen in wizard Q11. Threat modeling depth follows risk (`templates/threat-model.md`).

## Baseline controls (all projects)
- **Authentication and authorization:** use the approved mechanism (Q16); deny by default; role checks on the server for every protected action; least privilege for users, services, and CI tokens.
- **Input and output:** validate and encode at boundaries; parameterized queries; safe error responses (no stack traces or internals).
- **Sessions and secrets:** secure, expiring sessions; secrets only in the platform's secret store, never in git; rotate on exposure; environment-specific secrets.
- **Data protection:** TLS everywhere; encryption at rest for databases and backups; data minimization; defined retention and deletion; no real customer data in lower environments.
- **Dependencies and supply chain:** lockfiles; automated updates (`.github/dependabot.yml`); vulnerability scanning; review new dependencies (license, maintenance, necessity); pin CI actions by version (prefer commit SHA).
- **Logging and audit:** structured logs without secrets or personal data; audit trail for security-relevant actions where required.
- **CI/CD security:** least-privilege workflow permissions; production deploy requires environment approval; no secrets in build logs.
- **Incident response:** `docs/operations/runbooks/security-incident.md`.

## Additional for personal or regulated data (Q11 = B or C)
Documented lawful basis and privacy notice; data inventory and flow diagram; deletion/export processes; access logging; vendor due diligence; formal threat model and pre-launch security review; specialist/compliance sign-off where regulation applies. Prefer certified third parties for payment or identity handling.

## Security exceptions
Only the Technical Owner approves them, time-boxed, logged (`docs/governance/exception-process.md`).
