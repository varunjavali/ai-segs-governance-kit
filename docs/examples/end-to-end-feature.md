# End-to-End Example: one feature from requirement to release

Fictional example: **FEAT-003 "Customer cancels an unshipped order"** in a modular monolith with modules `orders`, `billing`, `shared`. Names and dates are illustrative; documents/templates exist in this kit; application behavior, CI runs, approvals and release records described below are fictional. The wizard profile is generated only after adoption.

| Step | What happens | Artifact / evidence | Gate |
|---|---|---|---|
| 1. Discovery | Founder states support tickets about mistaken orders; success measure: 50% fewer cancel-related tickets in 60 days | Wizard Q01, Q03 in `docs/decisions/project-profile.md` | 0 |
| 2. Requirements | Journey "customer cancels order" added to critical journeys; ambiguity "can shipped orders be cancelled?" resolved by product owner: no | `docs/requirements/README.md` | 1 |
| 3. Scope | FEAT-003 added to the register for MVP 1; non-goal: partial cancellation | `docs/roadmap/feature-register.md` (see the example row) | 2 |
| 4. Architecture check | Uses existing module boundaries: `orders` -> `billing` public refund interface; no new modules; no ADR needed | `docs/architecture/modules.json` | 3 |
| 5. Task readiness | Tier T2. Developer + AI complete the seven-block prompt; module owner approves | `prompts/examples/FEAT-003-cancel-order.md` validated by `scripts/check_task_prompt.py` | 5 |
| 6. Understand and clarify | AI restates understanding, lists planned files, asks: "Should refund failure block cancellation?" Owner answers: refund failure leaves cancellation pending, never falsely cancelled; the acceptance criteria and API contract must document this before approval | Q&A in the task thread | workflow 1-2 |
| 7. Impact analysis | Files: `orders` use case and endpoint; contract: orders API gains a cancel operation (additive); journeys affected: order placement, order list; rollback: feature flag off | `templates/impact-analysis.md` filled in the PR | workflow 3 |
| 8. Plan and approve | Smallest plan: domain rule, use case, endpoint, tests; module owner approves | PR description | 5 |
| 9. Implement | Branch `feature/FEAT-003-cancel-order`; AI edits only `src/modules/orders/` and tests; `make verify` run after each step | Branch commits | - |
| 10. Verify | Unit, integration (fake billing), end-to-end tests pass; architecture guardrail green; regression subset green; refund idempotency test fails when idempotency code is removed (checked) | CI run link | workflow 7 |
| 11. Review | Reviewer checks diff = scope, no weakened tests, contract diff additive, owner of `orders` approves via CODEOWNERS; `pr-metadata` would pass only with a real approved canonical task and feature, completed sections/checklist, actual diff and substantive verification evidence; this example is not an approval | PR approvals | 6 |
| 12. Integrate | Squash merge to `main`; auto-deploy to Dev; register status -> Verified with evidence link | Register row updated | - |
| 13. Release candidate | Cut `release/1.2`; same artifact in QA; full regression and accessibility pass | Release checklist section A | 7 |
| 14. Staging | Promote to Staging; smoke tests and rollback rehearsal pass; Release Approver signs | Release checklist section B; gate log | 8 |
| 15. Production | Tag `v1.2.0`; production environment approval by a human Release Approver; deploy the same artifact | Gate log; release notes | 9 |
| 16. Post-release | Smoke test OK; error rate normal; one defect found (double refund on rapid retry) -> BUG-021 with regression test; improvement: add a concurrency test template to the testing strategy | `docs/registers/defect-log.md`, `docs/registers/improvement-register.md` | 10 |

## What would have gone wrong without the system
- AI "helpfully" adds partial cancellation and an email feature: blocked at Scope check (non-goals in block 4, register approval).
- AI imports `billing` internals directly: `scripts/check_architecture.py` fails the PR ("deep import").
- A developer deletes the flaky refund test to get green: reviewer checklist and PR template item catch it; CI cannot be bypassed because branch protection requires checks (once applied and verified).
