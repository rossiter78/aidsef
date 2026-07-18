#!/usr/bin/env python3
"""AIDSEF test-on-edit hook (PostToolUse).

After any edit to product code or tests, run the project's test suite
so the agent sees breakage immediately (the TDD rhythm: run the tests
constantly, not at the end).

Contract: the project defines its test command in scripts/test.sh
(created when a cloned project is set up for its language; the AIDSEF
template itself ships without one, so this hook is a silent no-op
until then).

Exit codes (Claude Code hook contract): 0 = quiet success; 2 = the
suite failed, with the failure tail on stderr shown to the agent.
"""
import json
import os
import subprocess
import sys

TEST_SCRIPT = os.path.join("scripts", "test.sh")
TIMEOUT_SECONDS = 540


def edited_path(payload) -> str:
    tool_input = payload.get("tool_input") or {}
    return (tool_input.get("file_path") or tool_input.get("notebook_path") or "").replace("\\", "/")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    path = edited_path(payload)
    # Only react to product code and tests - not docs, specs, or config.
    if not any(marker in path for marker in ("src/", "tests/")):
        return 0
    if not os.path.exists(TEST_SCRIPT):
        return 0  # project hasn't defined its test command yet

    try:
        result = subprocess.run(
            ["bash", TEST_SCRIPT],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        sys.stderr.write("AIDSEF test-on-edit hook: 'bash' not found; cannot run scripts/test.sh.\n")
        return 0  # environment problem, not a test failure - fail open
    except subprocess.TimeoutExpired:
        sys.stderr.write(f"AIDSEF test-on-edit hook: test suite exceeded {TIMEOUT_SECONDS}s and was stopped.\n")
        return 2

    if result.returncode != 0:
        tail = ((result.stdout or "") + "\n" + (result.stderr or "")).strip().splitlines()[-40:]
        sys.stderr.write(
            "Test suite FAILED after your edit (scripts/test.sh). Last lines:\n"
            + "\n".join(tail) + "\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
