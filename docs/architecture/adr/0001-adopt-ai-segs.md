# ADR-0001: Adopt AI-SEGS as the team engineering governance system

- Status: Proposed (becomes Accepted when the Technical Owner signs Gate 4 in `docs/governance/gate-log.md`)
- Date: YYYY-MM-DD
- Deciders: Technical Owner, Founder

## Context
The team uses AI coding assistants and has experienced inconsistent practices, divergent requirement interpretations, architectural drift, regressions, conflicting changes, and incomplete testing.

## Decision
Adopt the AI-SEGS starter kit: wizard-approved decisions, one workflow with approval gates, a seven-block task prompt, automated guardrails in CI, protected branches with code ownership, and a continuous-improvement loop.

## Consequences
- Positive: consistent standard, visible deviations, traceability, reduced regressions.
- Negative: some added process; mitigated by risk tiers (`docs/governance/workflow.md`) and incremental adoption (`README.md`).
- Risk: documented rules mistaken for enforced rules; mitigated by `docs/governance/enforcement-status.md`.

## Triggers to revisit
Review cadence indicators (`docs/governance/continuous-improvement.md`) show rising PR rework or review delay without fewer defects for two consecutive months.
