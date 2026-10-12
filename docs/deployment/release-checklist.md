# Release Checklist

Copy into the release PR/issue. Environment flow: Dev -> QA -> Staging -> Production.

## A. QA and release readiness (Gate 7)
- [ ] Release scope = approved features only (feature register statuses are Verified)
- [ ] Artifact built once, versioned `vX.Y.Z`, SHA recorded: ______
- [ ] Deployed to Dev and QA; full regression suite result linked
- [ ] Security checks (dependency audit, SAST, secrets) result linked; no unresolved critical/high findings or exception approved
- [ ] Accessibility and performance checks as planned: result linked (or N/A with reason)
- [ ] Database migrations reviewed; run on data copy in QA; backward-compatible with previous release
- [ ] Documentation, API contracts, runbooks, and release notes (`templates/release-notes.md`) updated

## B. Staging and production approval (Gates 8-9)
- [ ] Same artifact promoted to Staging; smoke tests pass
- [ ] Migration rehearsal and rollback rehearsal done (or N/A with reason)
- [ ] Monitoring, alerts, and dashboards in place for new behavior
- [ ] Rollback plan written; previous artifact version available: ______
- [ ] On-call/release owner named and available for 2 hours after release: ______
- [ ] Release Approver (human) sign-off recorded in `docs/governance/gate-log.md`

## C. Post-release (Gate 10)
- [ ] Production smoke tests pass
- [ ] Error rate, latency, and key business metrics normal for 1 hour (adjust to your SLOs)
- [ ] Defects, incidents, and lessons recorded in `docs/registers/`
- [ ] Feature register updated with release evidence
