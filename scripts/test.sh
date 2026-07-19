#!/usr/bin/env bash
# AIDSEF test contract (see scripts/README.md).
#
# The template's own suite covers the tooling in tools/ using only the
# Python standard library (no dependencies to install). A project cloned
# from this template replaces this file with its stack's test runner -
# keeping the contract: exit 0 only if all tests pass, and accept
# optional test-file paths to run a subset (the red proof depends on
# subset runs).
set -euo pipefail

# Git Bash on Windows: 'python3' can be the Microsoft Store stub that
# opens the Store instead of running Python - fall back to 'python'.
PY=python3
"$PY" -c 'import sys' >/dev/null 2>&1 || PY=python

if [[ $# -eq 0 ]]; then
  set -- tests/test_*.py
fi

status=0
for test_file in "$@"; do
  [[ -f "$test_file" ]] || continue
  echo "== $test_file"
  "$PY" "$test_file" || status=1
done
exit $status
