# Feature Register

Canonical feature list. Statuses: Proposed, Approved, Ready, In-Progress, In-Review, Verified, Released, Deferred, Rejected. MVP values: MVP1, MVP2, MVP3, Later, Non-goal. Approval values: Pending, Approved, Rejected. Work may start only when Approval = Approved (enforced by `scripts/check_feature_register.py` for Approved and active delivery states). Approved rows require a meaningful approval record reference; Verified/Released rows require verification/release evidence as well. Metadata never authenticates an approver. The header and mandatory field rules are defined by `scripts/check_feature_register.py`. Use `Bootstrap-empty: yes` only before Gate 2 for a valid canonical table with no rows; remove it once project scope is agreed. An absent file/header/table is never a valid bootstrap.

Add each feature's detail (requirements, acceptance criteria, data, integrations, risks) in `docs/requirements/` using `templates/feature.md`, and link it in the Title cell or Evidence cell.

| ID | Title | User value | MVP | Priority | Modules | Quality attrs | Depends on | Test requirements | Owner | Approval | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FEAT-003 | EXAMPLE (delete at Gate 2): Customer cancels an unshipped order | Customers fix mistakes without contacting support | MVP1 | Should | orders, billing | Reliability, Security | - | Unit (cancel rules), integration (refund), E2E (cancel journey) | (name) | Pending | Proposed | - |
