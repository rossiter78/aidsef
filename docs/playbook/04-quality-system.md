# AIDSEF — Quality system

> Section 4 of the AIDSEF playbook. Decided 2026-07-18.
> Design principle: **every quality claim is mechanically verifiable, not promised.**

## 1. Tests-first, enforced by machinery

The rule is simple: the test that proves a piece of code works must exist — and fail — *before* the code is written. That's [TDD](../glossary.md#tdd-test-driven-development) (test-driven development). Most teams claim to do it; AIDSEF makes it impossible to skip.

### 1.1 The red proof (a required automated check)

Every task [branch](../glossary.md#branch) begins with a commit containing only test changes. The `red-proof` job in [CI](../glossary.md#ci-continuous-integration) — the automated check system that runs on every pull request — then does two things:

1. Runs the new tests against the codebase **as it was before the change** → verifies they **fail** (proving the tests actually demand something that didn't exist yet).
2. Runs them against the codebase **with the change** → verifies they **pass**.

This is publicly verifiable evidence that the tests came first and genuinely test the change. It cannot be faked — by human or AI — and merging is physically blocked until it passes.

> **Software Engineering Validation:** Auditable TDD (Beck). The red proof turns "we practice TDD" from a cultural claim into a falsifiable, re-runnable CI artifact: tests demonstrably fail on base and pass on head. It is a required status check under branch protection.

### 1.2 Role separation (enforced twice)

- A [hook](../glossary.md#hook) — a rule wired into the AI's tooling that physically blocks an action — stops the **Coder** from editing anything in `tests/**`, and stops the **Test Engineer** from editing anything in `src/**`. The AI writing the code literally cannot rewrite the tests to make its own life easier.
- A CI check backs it up: after the first test commit, test files are append-only. Any modification to an existing test assertion flags the pull request for mandatory human review.

### 1.3 Traceability matrix (generated, required check)

Nothing in the spec is allowed to silently go untested:

- Every [Given/When/Then](../glossary.md#givenwhenthen) criterion in `spec.md` carries an ID (e.g. `AC-012`).
- Every acceptance test declares which IDs it covers.
- CI generates the requirement→test table (`docs/traceability/<feature>.md`) and **fails the pull request if any criterion is uncovered**.

> **Software Engineering Validation:** Requirements traceability — a regulated-industry norm (think DO-178C/IEC 62304 lineage) — generated automatically on every PR rather than maintained by hand. Uncovered acceptance criteria are a hard CI failure, not a report finding.

### 1.4 Coverage gates (constitution defaults)

[Coverage](../glossary.md#coverage) measures what percentage of the code is actually exercised by tests:

- Project floor: **80%** of all lines.
- Lines changed in a pull request: **90%**.
- Both tunable per-project in `constitution.md`.

### 1.5 Mutation testing — high-risk only

Coverage can be gamed: a test can run code without checking anything. [Mutation testing](../glossary.md#mutation-testing) catches that — it deliberately introduces small bugs into the code and verifies the tests notice. If a "mutant" survives, the tests weren't really testing. Because it's computationally expensive, it runs as a required check **only on pull requests labeled `risk:high`** — the strongest available proof that the tests are real, applied exactly where it matters most, at bounded cost.

> **Software Engineering Validation:** mutmut / Stryker / PIT per language, scoped to `risk:high` PRs as a required check. Mutation score is the anti-vacuous-coverage metric; restricting it to the high-risk tier bounds CI cost while putting the strongest evidence where the blast radius is largest.

## 2. Review loop

### 2.1 What the AI reviewer must produce

Structured findings only — no vibes. Every finding has the same shape:
`{ category, severity, file:line, summary, concrete failure scenario }`

Categories: `correctness`, `security`, `design-drift`, `test-quality`, `simplicity`, `docs`.

Two categories deserve translation:
- `design-drift` — the implementation quietly diverged from what `design.md` and the ADRs said would be built. This catches "the AI did something else without telling anyone."
- `test-quality` — includes detecting **vacuous tests**: assertions that cannot fail, or tests so wrapped in stand-ins ([mocks](../glossary.md#mock)) that they no longer test anything real.

### 2.2 Arbiter triage

Each finding is classified, with written reasoning posted alongside:
- `blocking` — merge barred until addressed
- `fix-now` — worth the cost; the task returns to the build loop on the same branch
- `deferred` — real but not now; auto-filed as a backlog issue linking the pull request
- `rejected` — cost exceeds benefit; reasoning recorded

Hard rules (written into the constitution):
1. Confirmed `correctness` or `security` findings are always at least `fix-now` — they can never be cost-benefited away.
2. A human reply outranks any Arbiter classification.

### 2.3 Iteration cap: 2 cycles

Review → fix → re-review → fix. If findings still remain after the second cycle, the pull request parks as `needs-human`. A review loop that won't converge usually means the task or the design has a problem a human should see — so non-convergence is treated as signal, and counted in the retros.

## 3. Human review by risk tier (from §1 of the playbook)

- **High:** human review required before merge, plus AI review, plus the mutation check.
- **Standard:** AI review + CI required; humans spot-check a sample after merge (sampling rate set in the constitution, default 20%).
- **Low:** AI review + CI.

## 4. What the retro loop consumes from this system

Escalation rates, review-finding categories that keep recurring, triage calls humans overrode, red-proof failures, coverage trends, mutation scores. Recurring patterns become proposed amendments to the constitution or the role charters — always delivered as pull requests a human approves.
