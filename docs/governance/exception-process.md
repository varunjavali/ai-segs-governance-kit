# Exception Process

Criteria are never silently bypassed. If a rule cannot be met, request an exception.

1. Copy `templates/exception-request.md` into the PR (or a file under `docs/decisions/`).
2. State the rule, reason, risk, compensating control, **expiry date**, and the plan to remove the exception.
3. Approval: Technical Owner for architecture/security/data/production safeguards; reviewer for other rules. AI cannot approve.
4. Log it in `docs/registers/risk-log.md` (and `docs/registers/technical-debt-register.md` if it creates debt) with the expiry.
5. Expired exceptions are reviewed weekly; they are closed or renewed with a new approval.

Never acceptable exceptions: committing secrets, deleting tests to pass CI, releasing to production without Gate 9, or bypassing branch protection.
