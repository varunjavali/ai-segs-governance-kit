# Definition of Ready and Definition of Done

Exceptions are documented and approved (`docs/governance/exception-process.md`); they are never silent.

## Definition of Ready (checked at Gate 5)
- [ ] Approved objective and scope; non-goals stated
- [ ] Linked canonical approved task in `prompts/tasks/`; FEAT tasks also have an approved row in `docs/roadmap/feature-register.md`; bugs/changes/debt link their appropriate supporting records
- [ ] Acceptance criteria are observable and testable (at least two)
- [ ] Dependencies and affected modules identified; relevant architecture and contracts linked
- [ ] Security and data assessment done (data touched, authentication/authorization effect, new secrets)
- [ ] Impact analysis complete (`docs/governance/change-impact-checklist.md`)
- [ ] Verification plan defined (which tests, which regression checks)
- [ ] Risk tier assigned and required approvals obtained
- [ ] Seven-block prompt complete (`prompts/seven-block-prompt.md`)

## Definition of Done (checked at Gate 6, evidenced in the PR)
- [ ] Implementation matches approved scope; no unapproved changes
- [ ] All required automated checks and tests pass (output linked)
- [ ] Relevant existing functionality regression-tested
- [ ] Code review complete; reviewer confirmed contracts and dependencies
- [ ] Security, accessibility, and performance checks done where the plan requires them
- [ ] Documentation, contracts, ADRs, and the feature register updated
- [ ] No unresolved critical defects; remaining risks and exceptions recorded and approved
- [ ] Release and operational needs addressed (migration, config, alerts, runbook) where applicable
