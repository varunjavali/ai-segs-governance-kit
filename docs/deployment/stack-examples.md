# Stack-Specific Examples (to adapt at Gate 4)

> These are **examples that were not executed in this kit's build environment** (no application stack or network was available). Run and correct them against your real project, then replace this note with the confirmed commands. The stack is chosen in wizard Q13.

## Example A: TypeScript / Node.js (npm) on GitHub Actions
Add to `.github/workflows/` as a new job or file, and add its job name to the required status checks:
```yaml
  app-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20", cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm run test:ci
      - run: npm audit --audit-level=high
```
Prerequisites: supply package.json, a committed npm lockfile, and runner-specific `lint` and `test:ci` scripts. `test:ci` must run once and fail on failures; `--ci` is not a universal test-runner option. Specify approved tool versions and Node support in the project ADR; the example Node version is not a production stack decision.

Local commands to document in the README: `npm ci`, `npm run lint`, `npx tsc --noEmit`, `npm test`. Optional extra layers: `dependency-cruiser` or `eslint-plugin-boundaries` to complement `scripts/check_architecture.py`; `npx @redocly/cli lint openapi.yaml` and an OpenAPI diff tool for contract checks; `npx playwright test` for end-to-end journeys; `@axe-core/playwright` for accessibility.

## Example B: Python (pip) on GitHub Actions
Prerequisites: supply pinned requirements.txt and requirements-dev.txt including ruff, mypy, pytest and pip-audit, project configurations, and real application tests. These examples are conditional commands, not an installed stack.
```yaml
  app-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12", cache: pip }
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check .
      - run: mypy src
      - run: pytest -q
      - run: pip-audit -r requirements.txt
```
Optional: `import-linter` to complement the module guardrail; `schemathesis` for API contract tests; `locust` for load tests.

## Migration validation example (any stack)
In QA/Staging CI: restore the latest anonymized snapshot to a scratch database, run forward migrations, run the integration suite, then run the previous release's integration suite against the migrated schema (proves backward compatibility), and record timings.

## Smoke test example (after each deploy)
`GET /health/ready` returns 200; sign in as a synthetic user; run the one-step critical journey; fail the pipeline and trigger rollback if any step fails.

## Artifact versioning example
Name `app-<semver>-<git-sha>`; build once on merge to `main`; store in the registry; promotion jobs reference the artifact id and never rebuild.
