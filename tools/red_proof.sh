#!/usr/bin/env bash
# AIDSEF red proof (playbook section 4.1.1).
#
# Mechanical, re-runnable evidence that a change's tests came first and
# genuinely test the change:
#
#   1. The new/changed tests must FAIL against the base code (red) -
#      proving they demand something that didn't exist yet.
#   2. The same tests must PASS against the head code (green).
#
# Also enforces: implementation changes (src/**) with no new or changed
# tests are an automatic failure, and a branch whose first commit mixes
# test and product changes loses its tests-first evidence.
#
# Usage: tools/red_proof.sh BASE_SHA HEAD_SHA
# Requires: git, bash, and the project's test contract scripts/test.sh
# (which must accept optional test-file paths to run a subset).
set -euo pipefail

BASE_SHA="${1:?usage: red_proof.sh BASE_SHA HEAD_SHA}"
HEAD_SHA="${2:?usage: red_proof.sh BASE_SHA HEAD_SHA}"

MERGE_BASE="$(git merge-base "$BASE_SHA" "$HEAD_SHA")"
CHANGED="$(git diff --name-only --diff-filter=ACMR "$MERGE_BASE" "$HEAD_SHA")"
CHANGED_TESTS="$(printf '%s\n' "$CHANGED" | grep -E '^tests/' || true)"
CHANGED_SRC="$(printf '%s\n' "$CHANGED" | grep -E '^src/' || true)"

if [[ -z "$CHANGED_SRC" && -z "$CHANGED_TESTS" ]]; then
  echo "Red proof: no product or test changes - not applicable (docs/chore change). PASS."
  exit 0
fi

if [[ -n "$CHANGED_SRC" && -z "$CHANGED_TESTS" ]]; then
  echo "Red proof FAILED: implementation changed (src/**) but no tests were added or changed." >&2
  echo "AIDSEF is tests-first (constitution section 1.1): write the failing test, then the code." >&2
  exit 1
fi

if [[ ! -f scripts/test.sh ]]; then
  echo "Red proof FAILED: tests changed but scripts/test.sh (the project's test contract) is missing." >&2
  exit 1
fi

# --- Evidence 1: the branch's first commit touches only tests/ -------------
FIRST_COMMIT="$(git rev-list --reverse "$MERGE_BASE..$HEAD_SHA" | head -n 1)"
if [[ -n "$FIRST_COMMIT" ]]; then
  FIRST_FILES="$(git diff-tree --no-commit-id --name-only -r "$FIRST_COMMIT")"
  NON_TEST_FIRST="$(printf '%s\n' "$FIRST_FILES" | grep -vE '^tests/' || true)"
  if [[ -n "$NON_TEST_FIRST" ]]; then
    echo "Red proof FAILED: the branch's first commit ($FIRST_COMMIT) must contain only test changes." >&2
    echo "Non-test files in first commit:" >&2
    printf '  %s\n' $NON_TEST_FIRST >&2
    exit 1
  fi
fi

# --- Evidence 2: modified pre-existing tests flag for human review ---------
EXISTING_MODIFIED="$(git diff --name-only --diff-filter=M "$MERGE_BASE" "$HEAD_SHA" -- 'tests/' || true)"
if [[ -n "$EXISTING_MODIFIED" ]]; then
  echo "NOTICE: pre-existing test files were modified (append-only rule, playbook 4.1.2):"
  printf '  %s\n' $EXISTING_MODIFIED
  echo "REDPROOF_TESTS_MODIFIED=true" >> "${GITHUB_OUTPUT:-/dev/null}"
fi

# --- Evidence 3: red on base ------------------------------------------------
WORKDIR="$(mktemp -d)"
trap 'git worktree remove --force "$WORKDIR" 2>/dev/null || true; rm -rf "$WORKDIR"' EXIT
git worktree add --detach "$WORKDIR" "$MERGE_BASE" >/dev/null

# Overlay the head's changed tests onto the base code.
while IFS= read -r test_file; do
  [[ -z "$test_file" ]] && continue
  mkdir -p "$WORKDIR/$(dirname "$test_file")"
  git show "$HEAD_SHA:$test_file" > "$WORKDIR/$test_file"
done <<< "$CHANGED_TESTS"

# Base may predate scripts/test.sh - fall back to the head's copy.
if [[ ! -f "$WORKDIR/scripts/test.sh" ]]; then
  mkdir -p "$WORKDIR/scripts"
  git show "$HEAD_SHA:scripts/test.sh" > "$WORKDIR/scripts/test.sh"
fi

echo "Red proof: running changed tests against BASE ($MERGE_BASE) - expecting FAILURE..."
if (cd "$WORKDIR" && bash scripts/test.sh $CHANGED_TESTS); then
  echo "Red proof FAILED: the new/changed tests PASS against the base code." >&2
  echo "They demand nothing that didn't already exist - they do not test this change." >&2
  exit 1
fi
echo "Red proof: tests fail on base as required (red confirmed)."

# --- Evidence 4: green on head ---------------------------------------------
echo "Red proof: running changed tests against HEAD - expecting SUCCESS..."
if ! bash scripts/test.sh $CHANGED_TESTS; then
  echo "Red proof FAILED: the changed tests do not pass against the head code." >&2
  exit 1
fi

echo "Red proof PASSED: tests demonstrably fail on base and pass on head."
