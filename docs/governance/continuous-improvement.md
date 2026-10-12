# Monitoring, Learning, and Continuous Improvement

## Engineering-health indicators (reviewed monthly by the Technical Owner)
Build and test success rate - regressions and escaped defects - PR rework (review rounds) - failed deployments and time to recover - time spent correcting AI-generated mistakes - repeated architecture or security violations - review delay and delivery lead time - production reliability and performance - developer confidence and recurring friction (short monthly survey).

These improve the **system**. They are never used to rank developers, and lines of AI-generated code is not a metric.

## After a significant defect or incident
1. Blameless review within 5 working days (`templates/incident-postmortem.md`).
2. Root cause (5 whys).
3. Decide the fix category: improve **instructions** (AGENTS.md), **automated check** (scripts/CI), **architecture** (ADR), **training**, or **workflow**. Prefer an automated check over a reminder.
4. Record in `docs/registers/defect-log.md` and `docs/registers/improvement-register.md` with owner and due date.

## Changing governance rules
Pull request to the governance files with the reason and evidence, approved by the Technical Owner, noted in an ADR when it changes a principle. Remove rules that add bureaucracy without preventing real problems.

## Cadence
Weekly integration review - monthly indicator review and dependency/cost review - quarterly technical-debt and governance review - after every release Gate 10.
