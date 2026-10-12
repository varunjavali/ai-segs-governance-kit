# Team and AI-Agent Coordination (up to 10 developers)

## Ownership
- **Module ownership:** every module in `docs/architecture/modules.json` has one owning team or person; `.github/CODEOWNERS` declares review owners; enforcement needs real identities and verified branch protection.
- **Cross-cutting owners** (named in `docs/team/roles-and-ownership.md`): architecture, security, testing/QA, shared components and design system, operations/release.

## Tasks and branches
- One task = one branch = one PR. Branches are short-lived (aim for under 3 days), named `feature/FEAT-123-short-name`, `fix/BUG-45-short-name`, `chore/...`.
- Task assignment and dependencies are tracked in `docs/roadmap/feature-register.md` ("Depends on") and the issue tracker; no task starts before Gate 5.
- Rebase on `main` daily; integrate small and often to avoid long-lived divergence.

## Concurrent AI agents
1. Declare scope (modules/files) in the task prompt block 4.
2. Agents run in separate branches or git worktrees; never in the same working directory.
3. Parallel work is allowed only when scopes do not overlap and no shared file is touched. Tightly coupled tasks run sequentially.
4. Shared assets - configuration, design tokens, schemas, contracts, common utilities, `modules.json`, CI files - are edited only by their owners or by a task that explicitly owns them, and only one such task may be open at a time per asset.
5. Do not add agent-orchestration tooling until these basic controls work reliably.

## Integration checkpoints
- Daily: main is green; failing main is fixed first (stop-the-line).
- Per PR: required checks, code-owner review, up-to-date with main before merge.
- Weekly: 30-minute integration review - open PRs, conflicts, shared-file queue, escalations.

## Conflict resolution
Stop - identify the owner of each side - owner(s) decide - if still unresolved, Technical Owner decides and records an ADR when it affects architecture.

## Documentation duties
Authors update docs, contracts, ADRs, and the feature register in the same PR. Reviewers block merge if they are stale. Technical Owner audits docs monthly.

## Traceability
Requirement -> feature id (FEAT-nnn) -> task prompt (`prompts/tasks/`) -> branch/PR (PR must reference the id; checked by `scripts/check_pr.py`) -> tests -> review -> release record. Evidence is linked in the feature register.
