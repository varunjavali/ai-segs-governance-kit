# AI-Assisted Software Engineering Governance System (AI-SEGS) - Starter Kit

A guided, architecture-first, quality-enforced way for up to 10 developers (or more) and AI coding agents to build web and mobile applications with one consistent standard.

It is delivered as three integrated components:

| Component | What it is | Where |
|---|---|---|
| **A. Guided Project Wizard** | 25 questions, one at a time, with options, trade-offs and recommended defaults. Records proposals for human approval. | `docs/wizard/`, `scripts/wizard.py`, `prompts/wizard-facilitator-prompt.md` |
| **B. Governance and AI Development Playbook** | Workflow, seven-block prompt, 11 approval gates, decision authority, skill-aware guidance, coordination rules. | `docs/governance/`, `prompts/` |
| **C. Enforced Repository Starter Kit** | Real files and scripts: architecture guardrails, PR checks, CI, CODEOWNERS, templates, runbooks, branch-protection script. | `scripts/`, `.github/`, `src/`, `tests/`, `docs/` |

The wizard records **proposals and assumptions**; the playbook defines **process**; the scripts and repository settings **enforce** what can be enforced. What is enforced and what is only a checklist is stated honestly in [`docs/governance/enforcement-status.md`](docs/governance/enforcement-status.md).

## Quick start (founder or team lead)
1. Create a repository from these files and make `main` the default branch.
2. **Run the wizard** (`make wizard`, or paste [`prompts/wizard-facilitator-prompt.md`](prompts/wizard-facilitator-prompt.md) into Claude). Decisions land in `docs/decisions/project-profile.md`.
3. **Sign Gates 0-3** in [`docs/governance/gate-log.md`](docs/governance/gate-log.md) (business, requirements, MVP scope, architecture and quality targets).
4. **Initialize the repository (Gate 4):** replace `@your-org/...` owners in `.github/CODEOWNERS` and `docs/architecture/modules.json`, register your real modules, add your stack's commands to CI (examples in [`docs/deployment/stack-examples.md`](docs/deployment/stack-examples.md)), then run `make setup-check` and `make verify`.
5. **Switch on repository protections:** `./scripts/configure_branch_protection.sh --apply OWNER/REPO main`, then `--verify` (requires the `gh` CLI and admin rights; not run in this kit's build environment).
6. **Work in tasks:** each task gets a seven-block prompt ([`prompts/seven-block-prompt.md`](prompts/seven-block-prompt.md)), approved at Gate 5, saved under `prompts/tasks/`.

## How a task flows
Understand -> Clarify -> Assess impact -> Plan -> **Approve** -> Implement -> Verify -> Review -> Integrate -> Release -> Learn. See [`docs/governance/workflow.md`](docs/governance/workflow.md) and a complete worked example in [`docs/examples/end-to-end-feature.md`](docs/examples/end-to-end-feature.md).

## Adopt incrementally (do not do everything on day one)
| Level | When | Turn on |
|---|---|---|
| 1 - Safety net | Day 1 | `AGENTS.md`/`CLAUDE.md`, PR template, protected `main`, `governance.yml` CI |
| 2 - Control | Week 1-2 | Wizard decisions, Gates 0-4, seven-block prompts, `modules.json` guardrail, feature register |
| 3 - Quality | Weeks 2-6 | Stack CI (lint, types, tests), contract tests, QA/Staging environments, release checklist |
| 4 - Operations | Before launch | Monitoring and alerts, SLOs, backup-restore drill, load test, runbook rehearsal |

## Repository map
```
README.md  AGENTS.md  CLAUDE.md  Makefile
.github/        CODEOWNERS, PR template, issue templates, workflows/governance.yml, dependabot.yml
docs/wizard/    questions.json (source) + WIZARD.md (generated)
docs/decisions/ wizard output (project-profile.md) and assumptions
docs/governance/ standard, workflow, gates, gate log, DoR/DoD, skill guidance, impact checklist,
                 coordination, git+environments, exceptions, improvement, enforcement status
docs/architecture/ decision guide (monolith/modular/microservices), quality attributes, guardrails,
                 modules.json, adr/
docs/{requirements,api,security,testing,deployment,operations,design-system,roadmap,team,registers,examples}/
prompts/        seven-block template, wizard prompt, tasks/, examples/
templates/      change request, exception, impact analysis, feature, runbook, post-mortem, release notes, threat model
scripts/        automated checks, wizard, branch-protection script
src/ tests/     sample modular-monolith skeleton and self-tests for the guardrails
```

## Commands
`make verify` - all governance checks (also run by CI) - `make wizard` - `make setup-check` (Gate 4) - `make render-wizard`.
Requires Python 3.9+, Bash and GNU Make for the make commands. Without Make, use `bash scripts/verify_all.sh` with `PYTHON` set to your Python executable. On Windows use Git Bash; Python remains a native executable. `docs/governance/enforcement-status.md` lists the exact verification state of every control; `docs/governance/verification-report.md` records what was and was not run when this kit was built.

Pull requests use the [PR template](.github/pull_request_template.md). Record the commands you ran and their results so reviewers can assess the verification evidence.

## Known limits
- The sample `src/` is a skeleton to demonstrate the module guardrail; it is not your application.
- Stack-specific CI commands are examples that must be run against your real project at Gate 4.
- GitHub settings (branch protection, environments, required reviewers) exist only after someone applies and verifies them.
