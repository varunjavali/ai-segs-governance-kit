# Engineering Standard

One standard for everyone. Experience level changes how much **guidance and review** a person receives, never which safeguards apply.

## Principles
Business value first - architecture before implementation - simplicity before complexity - evolutionary architecture - secure and reliable by design - quality through automation - small, controlled changes - test before integration - documentation as a deliverable - one source of truth - human accountability - evidence over assumptions - continuous improvement.

## Evidence rule
Nobody (human or AI) states that a test, review, scan, or deployment succeeded unless they ran it and can show the output. "Not run" is an acceptable, honest status; a false "passed" is a process violation.

## Authority hierarchy
The canonical hierarchy and conflict rule are in [AGENTS.md](../../AGENTS.md#2-authority-order-higher-wins-never-silently-override).

A lower level never silently overrides a higher one. A conflict is reported, not resolved quietly.

## Decision categories
| Category | Examples | Who decides |
|---|---|---|
| AI-authorized | Naming, local code structure, test cases within approved scope and existing conventions | AI may decide; reviewer sees it in the diff |
| Developer / reviewer approval | Normal feature changes, material implementation trade-offs, adding a dependency, assumptions about non-critical behavior | The assigned developer and a reviewer |
| Technical Owner or Release Approver | Architecture changes, new modules or dependency directions, security exceptions, significant data migrations, changes to production safeguards (alerts, backups, access), production releases | Named Technical Owner / Release Approver (`docs/team/roles-and-ownership.md`) |

An AI agent never approves its own high-risk decisions, never presents a proposal as an approved decision, and never merges to a protected branch or releases to production.

## One source of truth
Each rule or decision lives in exactly one canonical file; every other document links to it. Canonical locations: rules for agents `AGENTS.md`; process `docs/governance/workflow.md`; gates `docs/governance/gates.md`; module boundaries `docs/architecture/modules.json`; scope `docs/roadmap/feature-register.md`; decisions `docs/architecture/adr/`.

## Changing this system
Governance changes follow the same path as code: pull request, review by the Technical Owner, version-controlled, with a recorded reason (`docs/governance/continuous-improvement.md`).
