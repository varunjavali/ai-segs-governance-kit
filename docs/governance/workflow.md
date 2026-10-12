# Standard Coding Workflow (mandatory for every task, human or AI)

| # | Step | What happens | Output | Stop and escalate if |
|---|---|---|---|---|
| 1 | **Understand** | Read `AGENTS.md`, the task, relevant architecture, code, and current status | Written understanding | Instructions are missing or contradictory |
| 2 | **Clarify** | List missing requirements, assumptions, conflicts, risks; ask targeted questions | Questions and documented assumptions | An assumption affects architecture, data, security, business behavior, or release risk |
| 3 | **Assess impact** | Complete `docs/governance/change-impact-checklist.md` | Impact analysis | Impact crosses modules owned by others or touches contracts, data, or security |
| 4 | **Plan** | Smallest coherent implementation and verification plan | Plan (files, tests, rollback) | Plan needs unapproved scope |
| 5 | **Approve** | Human approval at Gate 5 (who: see tiers below) | Approved seven-block prompt | - |
| 6 | **Implement** | Change only approved scope, follow conventions, small commits | Branch with focused diff | Scope grows, architecture surprise, conflict with another developer's work |
| 7 | **Verify** | Run tests, regression checks, security checks, quality gates (`make verify` plus stack commands) | Real command output | A failing test tempts you to weaken it - fix the cause or escalate |
| 8 | **Review** | Author self-reviews the full diff; reviewer inspects diff, contracts, dependencies, docs | Review approval (Gate 6) | Reviewer finds an unapproved change |
| 9 | **Integrate** | Merge via pull request after required checks and reviews pass | Merged PR | Any required check is red |
| 10 | **Release** | Promote one immutable build Dev -> QA -> Staging -> Production under Gates 7-9; verify deployed behavior | Release record | Smoke test fails: roll back |
| 11 | **Learn** | Record defects, operational findings, follow-up work; update registers (Gate 10) | Updated registers/docs | Same problem recurs: improve instruction, check, or architecture |

## Risk tiers (proportionate control)
| Tier | Typical change | Seven-block prompt | Gate 5 approver | Review | Notes |
|---|---|---|---|---|---|
| T0 Trivial | Typo, comment, docs wording | Not required (PR declares `Trivial-change: yes`) | None | CI must pass; 1 reviewer if CODEOWNERS applies | Never for code behavior, config, or dependencies |
| T1 Low | Isolated, well-tested change; no contract, data, security, or shared-file impact | Short form: all seven blocks, one or two lines each, in the PR/task | Reviewer | 1 reviewer | |
| T2 Standard | Feature work, bug fixes with logic changes | Full, saved in `prompts/tasks/` | Reviewer or module owner | 1+ reviewers per code owners | Default tier when unsure |
| T3 High | Architecture, security, data migration, contracts, production safeguards, release | Full plus ADR/exception as needed | **Technical Owner / Release Approver** | Technical Owner + code owner | AI never approves |

When unsure, use the higher tier. The tier is written in the task and challenged by the reviewer if wrong.

## Escalation triggers (any one pauses work)
Material scope change - unexpected architectural requirement - data migration - security or privacy concern - conflict with another developer's or agent's work - repeated test failure with unclear cause - missing acceptance criteria.

Escalation path: developer -> module owner -> Technical Owner (`docs/team/roles-and-ownership.md`). Record the outcome in the task or an ADR.
