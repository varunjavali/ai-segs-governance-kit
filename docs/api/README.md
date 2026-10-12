# API and Data Contracts

Wizard Q17 decides the approach (default: contract-first, each module owns its data).

## Rules
1. The contract file (for example an OpenAPI file stored under the api docs folder, and JSON Schemas for events) is the source of truth; code conforms to it.
2. **Compatible changes** (additive: new optional fields, new endpoints) are allowed with review by the API owner.
3. **Breaking changes** (removed/renamed fields, changed types or semantics, stricter validation) require: change request, version bump or parallel version, consumer migration plan, Technical Owner approval.
4. A contract diff check runs in CI once the stack is chosen (example in `docs/deployment/stack-examples.md`).
5. Every cross-module call uses the module's public interface; tables are never shared between modules.
6. External calls define timeouts, retry policy, and idempotency keys for writes.
7. Authentication and authorization requirements are stated per endpoint.

## Contract index
| Contract | Owner module | Consumers | Version | Location |
|---|---|---|---|---|
| | | | | |
