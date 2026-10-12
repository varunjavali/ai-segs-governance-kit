# CLAUDE.md

@AGENTS.md

(If your tool does not expand the `@AGENTS.md` import above, open `AGENTS.md` and follow it exactly. It is the only copy of the rules.)

## Claude-specific working notes
- Use plan mode for Gate 5: present the restatement, planned changes, risks and impact analysis, then wait for approval before editing.
- Use sub-agents or parallel sessions only for independent scopes with no shared files (see `docs/governance/team-coordination.md`); give each its own branch or worktree.
- Prefer targeted edits over whole-file rewrites; keep diffs small and reviewable.
- Run `make verify` before declaring any task complete and quote the real result.
- When unsure whether a change needs escalation, treat it as needing escalation.
