# Change Impact and Regression-Prevention Checklist

Complete before modifying existing code (copy into the PR or use `templates/impact-analysis.md`). The AI must produce it at workflow step 3.

- [ ] **Files/modules likely to change** listed; owners identified
- [ ] **User journeys and features** that could be affected (map to regression tests)
- [ ] **Contracts:** API, database schema, events, integrations - what changes, who consumes, compatibility plan
- [ ] **Quality attributes:** reliability, performance, security, accessibility, scalability implications
- [ ] **Required tests and regression checks** named (new and existing)
- [ ] **Shared files / concurrent work at risk** (config, design tokens, schemas, utilities, other open PRs)
- [ ] **Rollback and recovery:** how to undo; is any data change reversible; is the migration backward-compatible

## Regression-prevention rules
- Small, reviewable diffs; one concern per PR
- No unrelated refactoring, no unexplained interface changes
- Never delete or weaken a failing test to get green; fixing a bug requires a regression test that fails before the fix
- Never silently overwrite another developer's work; rebase and resolve conflicts with the owner
- Changes to shared components, tokens, schemas, or contracts require review by their owner (CODEOWNERS)
- Working functionality is protected by: automated tests on every PR, code review, version control, and the rollback procedure in `docs/operations/runbooks/failed-deployment-rollback.md`
