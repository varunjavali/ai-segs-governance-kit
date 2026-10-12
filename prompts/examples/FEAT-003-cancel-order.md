# Example task prompt (fictional; illustrates a completed seven-block prompt)

Task-ID: FEAT-003
Tier: T2
Gate-5-approval: Approved by Dana Reyes (orders module owner) 2026-03-02

## 1. Role
You are a senior backend engineer working in the `orders` module of a modular monolith. You follow `AGENTS.md`, respect `docs/architecture/modules.json`, and make the smallest coherent change.

## 2. Context
Customers cannot cancel an order after placing it, which generates support tickets (FEAT-003 in the feature register, MVP 1). Read first: `src/modules/orders/index.ts`, `src/modules/billing/index.ts` (public refund interface), and the project architecture ADR (not supplied here; ADR-0001 is a proposed governance adoption record). The `orders` module may depend on `billing` and `shared` only, through their public entry points. Orders have states: placed, paid, shipped, cancelled.

## 3. Objective
A signed-in customer can cancel their own order while it is not yet shipped, and is refunded automatically if it was paid.

## 4. Scope and non-goals
May change: `src/modules/orders/` (new cancel use case and endpoint), tests for it, and the orders section of the API contract. Must not change: `billing` internals, database tables owned by `billing`, `shared`, CI files, `modules.json`. Non-goals: partial cancellation, admin-initiated cancellation, cancellation emails (planned for FEAT-007).

## 5. Constraints
In the fictional application, use the `billing` public `refund` interface (the kit has only a demonstration stub); refunds must be idempotent (same order cancelled twice refunds once); authorization on the server (only the order's owner); no new dependencies; error responses must not expose internals; no hardcoded text outside the existing message catalog.

## 6. Acceptance criteria
- A placed or paid order owned by the caller can be cancelled; its state becomes cancelled after any required refund succeeds; on refund failure it remains pending for a bounded, idempotent retry.
- A paid order triggers exactly one refund even if the cancel request is repeated.
- A shipped order cannot be cancelled and returns a clear "cannot cancel" error.
- A caller who does not own the order receives a not-found response and nothing changes.
- Existing order placement and listing tests still pass unchanged.

## 7. Verification and handoff
Add unit tests for the cancel rules, an integration test with a fake billing interface, and an end-to-end test for the cancel journey. Run `make verify` and the stack test commands. Update the orders API contract and the feature register evidence. Handoff report per `AGENTS.md` section 7: changed files, test results (real output), risks (refund failure handling), assumptions, and what remains.
