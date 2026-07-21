---
name: aidsef-4-build
description: Phases 4–5 of the AIDSEF lifecycle. Reads one ready task issue. Produces failing tests first (Test Engineer, tests/**), then implementation (Coder, src/**) and the traceability matrix, delivered as a pull request that runs CI, AI review, and Arbiter triage.
argument-hint: [issue-number]
disable-model-invocation: true
---

# /aidsef-4-build — TDD build loop (Phases 4–5)

Run the build loop for one task issue: `$ARGUMENTS` — if empty, list `ready`-labeled issues via `gh issue list --label ready` and ask which one.

Two agents do the work under strict role separation — the hooks physically enforce it:
- **Test Engineer** (charter `.claude/agents/test-engineer.md`) — may not touch `src/**`
- **Coder** (charter `.claude/agents/coder.md`) — may not touch `tests/**`

Both read `constitution.md` first.

## Model routing

- **Local plane configured** (`.env` provides `AIDSEF_LITELLM_URL`; see `.env.example`): run each role as a headless Claude Code invocation on the local models —
  `AIDSEF_ROLE=coder ANTHROPIC_BASE_URL=<litellm-url> claude -p "<task prompt>" --model coder` (aliases `testwriter`/`coder` resolve in `litellm/config.yaml`). `AIDSEF_ROLE` keys the role-separation hooks.
- **Fallback (local plane not yet built — Phase B pending):** spawn the `test-engineer` and `coder` subagents directly. Note on the PR that author-model and reviewer-model are the same family for this task — the cross-model review principle (constitution §4) is temporarily waived and this is recorded honestly.

## Steps

1. **Branch**: `task/<issue-number>-<slug>` off `main`. Comment on the issue that the build started; move it to `building` on the board if present.
2. **Red** — Test Engineer writes failing tests from the issue's `AC-*` criteria into `tests/**`, each annotated `Covers: AC-xxx`. Commit **tests only** (the red proof depends on the branch's first commit touching only tests). Run the suite; confirm the new tests fail. If any new test passes on the base code, it demands nothing — rewrite it.
3. **Green** — Coder implements in `src/**` until the task's tests pass, running the suite after each meaningful change (the post-edit hook automates this). **Attempt cap: 3.** On the third failure: stop, open a `needs-human` issue with the attempts and a diagnosis (model capability vs. task specification), label the task issue `needs-human`, and end this run. Escalation to `coder-escalated` (frontier Claude) happens only after a human replies `escalate` (constitution §7.3).
4. **Refactor & self-review** — with tests green: clean up, remove dead code, check scope (nothing outside the task). Tests stay untouched by the Coder.
5. **Pull request** — `gh pr create` titled from the issue, linking `Closes #<issue>`, mapping changes to the `AC-*` covered, carrying the task's `risk:*` label. CI (`ci`, `red-proof`) and `claude-review` run automatically.
6. **Triage** — when review findings arrive, run the **arbiter** (charter `.claude/agents/arbiter.md`) on them: classify each `blocking`/`fix-now`/`deferred`/`rejected` with written reasoning as a PR comment; file backlog issues for every `deferred`. Confirmed `correctness`/`security` findings are never below `fix-now`.
7. **Fix cycles** — for `blocking`/`fix-now`: Coder addresses them on the same branch (tests change only if the Test Engineer is re-engaged for a genuinely wrong test, via `needs-human`). **Cycle cap: 2** — findings still open after the second re-review park the PR as `needs-human`.
8. **Merge gate per constitution §3.3** — High: human review + approval required; announce and stop. Standard/Low: with AI review and all checks green, the merge may proceed (Standard is spot-checked post-merge). Never merge over a failing required check.

## Rules

- The tests are the specification. A Coder who disagrees with a test escalates; it never edits the test.
- Every stop (escalation, parked PR) is queueable: label it `needs-human`, summarize the state, move on.
