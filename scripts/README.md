# Scripts — the project's command contract

CI, the hooks, and the red proof are language-agnostic: they call these scripts instead of assuming a language. **A project cloned from this template replaces them for its stack during setup.** The template ships a `test.sh` that runs its own tooling tests (`tests/`, standard-library Python only) — replace it, keeping the contract below. `coverage.sh` is not shipped, so that check reports "not configured" and passes until the cloned project defines it.

| Script | Contract |
|---|---|
| `test.sh` | Run the test suite; exit 0 only if all tests pass. **Must accept optional test-file paths as arguments** to run a subset — the red proof depends on this. Example (Python): `pytest "${@:-tests/}"` |
| `coverage.sh BASE_REF` | Run tests with coverage; exit nonzero if project coverage < 80% or coverage of lines changed since `BASE_REF` < 90% (thresholds per constitution §2 — keep in sync if amended). |
| `setup-repo.sh` | One-time repository setup: labels, branch protection, Projects board (run by an agent after cloning; see the script's header). |

All scripts run under `bash` from the repository root, in CI (Ubuntu) and locally (Git Bash on Windows) alike.
