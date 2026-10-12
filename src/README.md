# src/

Skeleton of a modular monolith used to demonstrate and test the module guardrail (`scripts/check_architecture.py`). **It is not your application.** Replace the example modules with yours at Gate 3/4 and register them in `docs/architecture/modules.json` (needs an ADR and Technical Owner approval).

Rules in force here: modules import each other only as allowed in `modules.json` and only through the public entry point (`index.*`, `__init__.py`, or a `public/` folder). Business logic does not import web frameworks.
