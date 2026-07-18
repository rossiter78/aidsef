#!/usr/bin/env python3
"""AIDSEF role-separation hook (PreToolUse).

Physically blocks the wrong role from editing the wrong files
(constitution section 4):

  - coder          may not edit  tests/**
  - test-engineer  may not edit  src/**

The role is taken from argv[1] (used by the per-agent hooks in the
coder and test-engineer charters) or, failing that, from the
AIDSEF_ROLE environment variable (used by headless local-model runs).
No role -> nothing is blocked; this hook constrains the separated
roles, not humans or the orchestrator.

Exit codes (Claude Code hook contract): 0 = allow, 2 = block, with the
reason on stderr shown to the agent.
"""
import json
import os
import sys

FORBIDDEN = {
    "coder": ("tests/",),
    "test-engineer": ("src/",),
}


def main() -> int:
    role = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AIDSEF_ROLE", ""))
    role = role.strip().lower()
    if role not in FORBIDDEN:
        return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed input: fail open; CI role-separation check backs this up

    tool_input = payload.get("tool_input") or {}
    raw_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not raw_path:
        return 0

    # Normalize to a project-relative, forward-slash path.
    path = raw_path.replace("\\", "/")
    project = (payload.get("cwd") or os.getcwd()).replace("\\", "/").rstrip("/")
    if project and path.lower().startswith(project.lower() + "/"):
        path = path[len(project) + 1:]

    for prefix in FORBIDDEN[role]:
        if path.startswith(prefix) or ("/" + prefix) in path:
            sys.stderr.write(
                f"BLOCKED by AIDSEF role separation (constitution section 4): "
                f"the '{role}' role may not edit '{raw_path}'.\n"
                f"If you believe this file genuinely needs to change, open a "
                f"'needs-human' issue explaining why and stop this task - do "
                f"not try to work around the block.\n"
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
