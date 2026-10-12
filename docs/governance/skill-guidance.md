# Skill-Aware Developer Guidance and Escalation

One standard, different support. Reviewer attention and guidance depth scale with experience; permission to bypass safeguards does not.

| Level | Guidance provided | Review |
|---|---|---|
| Beginner | Step-by-step task packet (below), worked examples, pairing for first tasks, tasks sized to under one day | Full review by an intermediate/senior reviewer; Gate 5 approved by module owner |
| Intermediate | Task packet with links, not step-by-step; owns small modules | Standard review |
| Senior | Objective, constraints, and acceptance criteria; may be module owner and reviewer | Peer review; Technical Owner for T3 |
| Reviewer | Review checklist below | - |
| Technical Owner | Architecture and security decisions, exceptions, escalations (not every trivial change) | - |

## Task packet (what every developer receives with a task)
1. **Plain-language objective:** what the user can do after this change, in one paragraph.
2. **Concepts and prerequisites:** the 2-3 ideas needed (for example "what idempotent means").
3. **Project rules:** the exact sections of `AGENTS.md` and docs that apply; one existing example to copy.
4. **Exact commands and expected outcomes:** e.g. `make verify` should end with `ALL GOVERNANCE CHECKS PASSED`.
5. **Common mistakes and recovery:** see table below.
6. **Required tests** and how to read their failures.
7. **Escalation criteria:** the triggers in `docs/governance/workflow.md`.

## Common mistakes and recovery
| Mistake | Recovery |
|---|---|
| AI changed files outside scope | `git restore` those files; add the boundary to the Scope block; re-run the prompt |
| Architecture check fails with "may not depend on" | Do not edit `modules.json`. Move the logic or ask the module owner for a public interface; escalate if a new dependency is truly needed |
| Test fails after AI edit | Read the failure; fix the code, not the test. If the test is wrong, explain why in the PR and get reviewer approval |
| Merge conflict in a shared file | Stop; ask the file's owner; never "accept theirs/mine" blindly |
| Secret committed | Treat as compromised: rotate it, then follow `docs/operations/runbooks/security-incident.md` |
| Unsure of tier | Use the higher tier |

## Reviewer checklist
Diff matches the approved prompt - no unrelated changes - tests prove acceptance criteria and would fail without the change - no weakened tests - contracts and docs updated - module boundaries respected - security and data handling reasonable - AI handoff report matches what you see.

## Interpreting failures
Red CI means stop, not retry. Read the first failing check; identify whether it is the change, an existing flaky test (report it in `docs/registers/defect-log.md`), or the environment. Three failed attempts on the same failure: escalate.
