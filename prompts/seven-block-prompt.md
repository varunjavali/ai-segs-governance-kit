# Seven-Block AI Coding Prompt (canonical template)

Every significant coding task (tier T1 short form, T2/T3 full) uses these seven blocks. Copy this file to `prompts/tasks/<ID>-<short-name>.md`, fill every block, get Gate 5 approval, then give it to the AI. `scripts/check_task_prompt.py` rejects files with missing blocks, placeholders, or no approval.

If a critical block is incomplete, ambiguous, or contradictory, the AI **must ask targeted questions before coding**. For non-critical gaps it may propose documented assumptions, and must obtain approval where an assumption materially affects architecture, data, security, business behavior, or release risk.

**Before implementing, the AI must:** restate its understanding, list planned changes, identify risks, and request the required approval.

Header (required; replace the example values):

```
Task-ID: FEAT-000
Tier: T2
Gate-5-approval: Approved by <name> <YYYY-MM-DD>
```

## 1. Role
The expertise and responsibilities the AI takes on (for example "Senior backend engineer on the orders module, following AGENTS.md and the modular-monolith rules").

## 2. Context
Product need, existing code and files to read first, relevant architecture/ADRs/contracts, conventions, current behavior, links to the feature in the register.

## 3. Objective
The exact problem or outcome in one short paragraph, in user terms.

## 4. Scope and non-goals
May change: (modules/files). Must not change: (modules/files, contracts, shared assets). Non-goals: (adjacent things that tempt scope creep).

## 5. Constraints
Technology and versions, architecture rules (module boundaries), security and data rules, performance and compatibility limits, coding and design-system rules, no new dependencies without approval.

## 6. Acceptance criteria
Observable, testable conditions (at least two), written as a list. Include failure cases and permissions.

## 7. Verification and handoff
Tests to add or run, regression checks, security/accessibility/performance checks, `make verify`, review evidence required, the handoff report format from `AGENTS.md` section 7 (changed files, results, risks, remaining work), docs and contracts to update.
