#!/usr/bin/env bash
# Configure (and verify) GitHub branch protection with the gh CLI.
#   ./scripts/configure_branch_protection.sh OWNER/REPO main [release/1.0 ...]          # dry run: prints the plan
#   ./scripts/configure_branch_protection.sh --apply OWNER/REPO main                     # applies it
#   ./scripts/configure_branch_protection.sh --verify OWNER/REPO main                    # reads back and checks it
# Notes: legacy branch protection needs exact, existing branch names. For patterns such as release/*, create a
# repository ruleset in the GitHub UI with the same settings (see docs/governance/git-environment-governance.md).
# Required status checks must match the job names in .github/workflows/governance.yml.
set -euo pipefail

MODE=plan
case "${1:-}" in --apply) MODE=apply; shift ;; --verify) MODE=verify; shift ;; esac
REPO="${1:?usage: $0 [--apply|--verify] OWNER/REPO BRANCH [BRANCH...]}"; shift
[[ "$REPO" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || { echo "invalid OWNER/REPO" >&2; exit 2; }
[ "$#" -ge 1 ] || { echo "at least one branch required" >&2; exit 2; }
REVIEWS="${REVIEWS:-1}"

PY="${PYTHON:-python3}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
body() { "$PY" "$SCRIPT_DIR/check_branch_protection.py" --policy --reviews "$REVIEWS"; }
# Validate policy even for verify mode, before any API operation.
body >/dev/null

for BRANCH in "$@"; do
  ENCODED_BRANCH="$("$PY" -c 'import sys; from urllib.parse import quote; print(quote(sys.argv[1], safe=""))' "$BRANCH")"
  case "$MODE" in
    plan)  echo "[dry-run] would PUT repos/$REPO/branches/$ENCODED_BRANCH/protection with:"; body ;;
    apply) command -v gh >/dev/null || { echo "gh CLI required" >&2; exit 2; }
           body | gh api -X PUT "repos/$REPO/branches/$ENCODED_BRANCH/protection" --input - >/dev/null
           echo "applied protection to $BRANCH (now run with --verify)" ;;
    verify) command -v gh >/dev/null || { echo "gh CLI required" >&2; exit 2; }
           out="$(gh api "repos/$REPO/branches/$ENCODED_BRANCH/protection")"
           printf '%s\n' "$out" | "$PY" "$SCRIPT_DIR/check_branch_protection.py" --reviews "$REVIEWS" ;;
  esac
done
