#!/usr/bin/env bash
# Runs every governance check locally and in CI. Exit non-zero on the first failure.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
step() { printf '\n== %s ==\n' "$1"; }

step "wizard render in sync";      "$PY" scripts/render_wizard.py --check
step "docs consistency";           "$PY" scripts/check_docs.py
step "feature register";           "$PY" scripts/check_feature_register.py
step "task prompts";               "$PY" scripts/check_task_prompt.py
step "architecture guardrail";     "$PY" scripts/check_architecture.py
step "secret scan";                "$PY" scripts/scan_secrets.py
step "shell syntax";               for f in scripts/*.sh; do bash -n "$f"; echo "ok $f"; done
step "guardrail self-tests";       "$PY" -m unittest discover -s tests/governance -v
printf '\nALL GOVERNANCE CHECKS PASSED\n'
