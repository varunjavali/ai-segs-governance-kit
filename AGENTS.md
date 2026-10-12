# AGENTS.md - Rules for every AI coding agent and human developer

This is the **single canonical rule set** for AI agents (Claude, Copilot, Codex, Cursor, and others). `CLAUDE.md` imports this file; do not copy rules elsewhere - link here.

## 1. Before you touch code
1. Read this file, `docs/governance/workflow.md`, the task's seven-block prompt (`prompts/seven-block-prompt.md` format), `docs/architecture/modules.json`, and the code you will change.
2. If the task has no approved seven-block prompt (Gate 5) and is not tier T0/T1 (see `docs/governance/workflow.md`), **stop and ask** the developer to complete it.
3. Restate your understanding, list planned file changes, risks, and affected user journeys. **Wait for approval** before implementing.

## 2. Authority order (higher wins; never silently override)
1. Approved business requirements and acceptance criteria
2. Approved architecture decisions (ADRs) and quality requirements
3. Shared engineering standards and security policies (`docs/governance/`, `docs/security/`)
4. This file
5. The task prompt
6. Your own suggestions

If two sources conflict, **stop and report the conflict**; do not choose quietly. A proposal is not a decision: never describe something as "approved" unless a named human approved it in writing.

## 3. Stop and escalate (do not continue) when you find
- A scope change, a new feature, or an unapproved requirement
- An architecture change, new module, new dependency direction, or new infrastructure
- A data migration, schema change, or API/event contract change not in the approved plan
- A security or privacy concern, or a need for a new secret/credential
- Another developer's or agent's work overlapping yours
- Missing or contradictory acceptance criteria

## 4. Never
- Weaken, skip, delete, or rewrite a failing test to get a green build
- Perform unrelated refactoring or reformat files you were not asked to change
- Change protected files (see `.github/CODEOWNERS`) unless the task explicitly includes them
- Import across modules except as allowed by `docs/architecture/modules.json` (public entry points only)
- Commit secrets, credentials, personal data, or real customer data
- Add dependencies without stating name, version, license, and reason in the handoff
- Claim a test, scan, review, or deployment passed unless you ran it and can show the output
- Approve your own high-risk decisions, merge to protected branches, or release to production

## 5. Implementation rules
- Smallest coherent change; one concern per pull request. Follow existing conventions and patterns.
- Business logic stays out of framework/transport/infrastructure code where practical.
- Validate input at boundaries; fail safely; never expose internals in error responses.
- Every behavior change comes with a test; every bug fix comes with a regression test that failed before the fix.
- Keep documentation, contracts, and `docs/roadmap/feature-register.md` in step with the code.

## 6. Verify before you hand off
Run `make verify` (governance checks) plus the stack commands listed in `docs/deployment/stack-examples.md` for this project. Report real results.

## 7. Handoff format (end of every task)
Changed files (and why) - tests run and results - checks run and results - risks and assumptions - open questions - docs/contracts updated - what remains. Include the exact command output summaries; say "not run" for anything you did not run.

## 8. Parallel agents
Work only inside your declared file/module scope. Never edit shared config, design tokens, schemas, contracts, or common utilities unless your task owns them (`docs/governance/team-coordination.md`). Use a separate branch/worktree per agent.

## 9. Repository map
`docs/wizard/` decisions wizard - `docs/governance/` standards, gates, workflow - `docs/architecture/` modules, ADRs - `docs/roadmap/` MVPs and feature register - `prompts/` task prompts - `templates/` templates - `scripts/` automated checks - `src/` application - `tests/` automated tests.
