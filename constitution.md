# Constitution

The project rulebook: the engineering rules that are **not up for debate mid-project**. Every [agent](docs/glossary.md#agent) reads this document at the start of every task. Humans ratify it once, at project start; after that it changes only through a human-approved [pull request](docs/glossary.md#pull-request-pr) (see [§8 Amendments](#8-amendments)).

This file ships with the AIDSEF template as a ready-to-ratify default. Cloning a new project? Read it, tune the tables in §3–§6 if your project needs different thresholds, confirm the operating profile (solo is the default), and approve the PR that adds it. That approval **is** Phase 0 of the [lifecycle](docs/playbook/01-process-and-governance.md).

> **Software Engineering Validation:** This is a working agreement + engineering standards doc, versioned as code. Every agent receives it as context on every task; every change to it is a reviewed PR. The defaults below implement mechanically-enforced TDD, risk-tiered change control, and structured review triage as specified in the [playbook](docs/playbook/01-process-and-governance.md).

## Project settings

- **Operating profile: Solo** — one person wears all the hats (see §5). Moving to a team profile is an amendment (§8).
- **Autonomy level:** how much the AI does without you watching. It lives in **one** place — the `AIDSEF_AUTONOMY_LEVEL` variable in the repository's GitHub settings, **not** in this file — so there is only ever one switch to check. It starts at **0 — Watched**; see §6 for what the levels mean and when to raise it.

*(Who adopted this rulebook, and when, is recorded automatically by Git when the pull request that adds it is approved and merged — core rule 6. That approval is Phase 0; there is no form to fill in.)*

---

## 1. Core rules

1. **Tests come first, always.** No product code may be written before a failing test exists that the code must satisfy. This is [TDD](docs/glossary.md#tdd-test-driven-development) — and it is enforced by machinery, not honor: the [red proof](docs/glossary.md#red-proof) CI check and the role-separation [hooks](docs/glossary.md#hook) (§4).
2. **Every requirement must be phrased testably**, in [Given/When/Then](docs/glossary.md#givenwhenthen) form, with a unique ID (`AC-001`, `AC-002`, …). If it can't be phrased that way, it isn't ready to build.
3. **Significant technical decisions get a written record** — an [ADR](docs/glossary.md#adr-architecture-decision-record) in `docs/adr/`, listing the alternatives considered and why they lost. "Significant" means: hard to reverse, adds a [dependency](docs/glossary.md#dependency), or shapes how later work must be built.
4. **An uncertain or blocked agent asks, never guesses.** It opens a `needs-human` [issue](docs/glossary.md#issue) describing what it knows, what it tried, and what it needs — then stops that task and moves to unblocked work.
5. **Humans may veto at any gate at any time.** The tiers in §3 only set which gates *require* a human; nothing stops you from stepping in anywhere. A human decision always outranks an AI decision.
6. **If it isn't in Git, it didn't happen.** Specs, designs, decisions, reviews, retros — every work product lands in the repository. The [audit trail](docs/glossary.md#audit-trail) is the repository history itself.

## 2. Quality thresholds

| Threshold | Default | Where enforced |
|---|---|---|
| [Coverage](docs/glossary.md#coverage), whole project | **80%** of lines | `ci` required check |
| Coverage, lines changed in a PR | **90%** | `ci` required check |
| [Red proof](docs/glossary.md#red-proof) (new tests fail on base, pass on head) | Required on every feature/fix PR | `red-proof` required check |
| [Traceability](docs/glossary.md#traceability-matrix): every `AC-*` covered by ≥ 1 test | Required | `ci` required check |
| [Mutation testing](docs/glossary.md#mutation-testing) | Required on `risk:high` PRs only | CI, high-tier job |
| Review iteration cap | **2 cycles**, then the PR parks as `needs-human` | Review workflow |
| Post-merge human spot-check (Standard tier) | **20%** sample | Retro agent tracks |

## 3. Risk tiers and gates

Every change gets a [risk tier](docs/glossary.md#risk-tier) [label](docs/glossary.md#label) — `risk:high`, `risk:standard`, or `risk:low` — proposed by the Planner agent and stamped on the work item. **Any human can overrule it by changing the label**; raising anything to High immediately re-arms every human checkpoint for it.

### 3.1 Change classes

- **Feature** — building something new. Full lifecycle (Phases 1–6).
- **Fix** — repairing something broken. Abbreviated path: reproduce the bug with a failing test → fix → review → merge. Links back to the spec it corrects; no new spec.
- **Chore** — housekeeping (dependencies, docs, tooling). Skips Phases 1–3.
- **[Spike](docs/glossary.md#spike)** — a sanctioned throwaway experiment: exploring an idea, a library, or a design question where the goal is learning, not shipping. Spikes live on `spike/*` [branches](docs/glossary.md#branch), skip every gate and every test requirement — and in exchange **can never merge**: the `ci` required check automatically fails any pull request from a `spike/*` branch. What a spike learns is written down (in its issue, a spec draft, or an ADR); anything worth keeping is rebuilt through the normal lifecycle. Spikes carry no risk tier — the tier system governs what merges, and spikes don't.

### 3.2 Tier triggers (any one is enough)

| Tier | Triggers |
|---|---|
| **High** | Logins or permissions ([auth/authz](docs/glossary.md#authentication--authorization-authauthz)); payments or money movement; personal data ([PII](docs/glossary.md#pii-personally-identifiable-information)) or changes to how data is stored; public [API](docs/glossary.md#api-application-programming-interface) contracts other systems depend on; security or server configuration; adding a new third-party [dependency](docs/glossary.md#dependency); any change over 400 [lines of code](docs/glossary.md#lines-of-code-loc) |
| **Standard** | Ordinary feature or fix work matching neither High nor Low |
| **Low** | Documentation; adding tests without touching product code; formatting; mechanical cleanups under 50 lines that leave all test results unchanged |

### 3.3 Gate matrix

| [Gate](docs/glossary.md#gate) | High | Standard | Low |
|---|---|---|---|
| Spec approval | Human required (blocking) | Human required (batchable at your convenience) | Skipped / AI approves, human notified |
| Design approval | Human required (blocking) | AI self-review; human notified, one business day to object | Skipped |
| Merge approval | Human + AI review + all checks green + mutation check | AI review + green checks; 20% human spot-check after merge | AI review + green checks |

> **Software Engineering Validation:** Standard change-management risk classes mapped to phase gates. Enforcement is [branch protection](docs/glossary.md#branch-protection) with [required status checks](docs/glossary.md#required-status-check) (`ci`, `red-proof`, `claude-review`) — mechanical on public repos and paid plans; advisory-but-visible on Free-plan private repos (playbook §5.3).

## 4. Role separation

The nine roles and their hard limits are defined in the [charters](docs/glossary.md#charter) (`.claude/agents/`). Two limits are enforced by machinery, twice each:

- The **Coder may not edit tests** (`tests/**`). The **Test Engineer may not edit product code** (`src/**`). Enforced by [hooks](docs/glossary.md#hook) that physically block the edit, and backed by CI: after a task's first test commit, test files are append-only — modifying an existing test assertion flags the PR for mandatory human review.
- The **reviewer is never the author's twin**: the AI reviewing code must come from a different model family than the AI that wrote it ([cross-model review](docs/glossary.md#cross-model-review)).

## 5. Operating profile

This project runs the **solo profile**: one human wears all the hats. Gates arrive as GitHub approval requests. The daily loop: approve specs, skim designs, review high-risk PRs, overrule [triage](docs/glossary.md#triage) calls when you disagree.

Switching to the **team profile** is an amendment (§8): assign an approver of record per gate — spec → product owner; design → senior engineer; High-tier merge → senior engineer; constitution amendments → engineering lead.

## 6. Autonomy level

This project starts at [autonomy level](docs/glossary.md#autonomy-level) **0 — Watched**: the build loop runs in an interactive session you observe. The level lives in one place — the `AIDSEF_AUTONOMY_LEVEL` variable in the repository's GitHub settings, which the resident-runner workflow reads. Only a human changes it, and only when the trust milestones are met:

- **0 → 1 (Attended):** two consecutive features with zero red-proof failures and no surprise triage overrides.
- **1 → 2 (Resident):** escalation rate below 1 per 10 tasks, and you've stopped reading standard-tier changes line-by-line and started sampling them.

## 7. Review, triage, and escalation

### 7.1 Review findings

AI review findings are structured only — no vibes: `{ category, severity, file:line, summary, concrete failure scenario }`, with categories `correctness`, `security`, `design-drift`, `test-quality`, `simplicity`, `docs`.

### 7.2 Triage classes

The Arbiter classifies every finding, posting written reasoning alongside: `blocking` · `fix-now` · `deferred` (auto-filed as a backlog issue linking the PR) · `rejected` (reasoning recorded on the PR).

**Hard rules:**
1. Confirmed `correctness` or `security` findings are always at least `fix-now` — they can never be cost-benefited away.
2. A human reply outranks any Arbiter classification, no ceremony required.
3. After 2 review cycles with findings remaining, the PR parks as `needs-human`. Non-convergence is signal, not failure — it is counted in the retros.

### 7.3 Escalation (local → cloud model)

When the local Coder can't get the tests passing after **3 attempts**, it stops and opens a `needs-human` issue with what it tried and its diagnosis (model capability vs. badly-specified task). A human replies `escalate` (re-run on the frontier model) or `re-scope` (Planner splits the task). **Escalation never happens without a human's yes.** Every request and outcome is counted in the retros.

## 8. Amendments

- Any change to this constitution, to a role charter, **or to the enforcement machinery itself** — the [hooks](docs/glossary.md#hook) and settings in `.claude/`, the skills, and the [workflows](docs/glossary.md#workflow) in `.github/workflows/` — arrives as a pull request. **Amendment PRs are always human-approved** — no exceptions, at any autonomy level. An agent must never be able to loosen its own guardrails without a human's yes.
- The Retro agent proposes amendments when it spots recurring patterns; humans can propose them any time.
- An amendment takes effect when its PR merges. Agents always read the merged version.

> **Software Engineering Validation:** The framework improves itself under the same governance it applies to code — data-driven retrospectives whose output is constrained to auditable, human-approved PRs against this file or the charters. No silent drift.
