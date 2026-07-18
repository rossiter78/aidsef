# Hooks — the physical guardrails

A [hook](../../docs/glossary.md#hook) is a rule wired into the AI's tooling that fires automatically on certain actions and can physically block them. These are the "enforced by machinery, not honor" half of constitution §4. Requires Python 3 on the machine running Claude Code.

| Hook | Fires | Does |
|---|---|---|
| [check_role_paths.py](check_role_paths.py) | **Before** any file edit (PreToolUse) | Blocks the **Coder** from `tests/**` and the **Test Engineer** from `src/**`. The blocked agent is told to open a `needs-human` issue instead of working around it. |
| [run_tests_after_edit.py](run_tests_after_edit.py) | **After** any edit to `src/**` or `tests/**` (PostToolUse) | Runs the project's test suite (`scripts/test.sh`) so the agent sees breakage immediately. No-op until a cloned project defines that script. |

## How the role is known — enforced twice

1. **Per-agent hooks** in the [coder](../agents/coder.md) and [test-engineer](../agents/test-engineer.md) charters pass the role explicitly (`check_role_paths.py coder`) — covers interactive subagent runs.
2. **The project-wide hook** in [settings.json](../settings.json) reads the `AIDSEF_ROLE` environment variable — covers headless local-model runs, which set it (see `/aidsef-build`).

No role set → nothing is blocked: the hooks constrain the separated roles, not humans or the orchestrator. CI independently backs this up (test files are append-only after a task's first commit — playbook §4.1.2), so even a bypassed hook can't slip through unreviewed.

> **Software Engineering Validation:** Defense in depth for role separation: local enforcement at the tool boundary (deterministic, pre-action) plus a CI invariant on the artifact (append-only tests after the red commit). Phase C's acceptance test deliberately attempts to violate both.
