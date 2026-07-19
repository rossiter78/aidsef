# AIDSEF — Process flow & governance

> Section 1 of the AIDSEF playbook. Decided 2026-07-18.
> Core principle: **every work product is saved in [Git](../glossary.md#git); every decision checkpoint is a [pull request](../glossary.md#pull-request-pr).**
> The [audit trail](../glossary.md#audit-trail) is not a report bolted onto the process — it *is* the repository history.

## 1. Lifecycle overview

Every feature moves through seven phases. Each phase produces a written document that gets saved in Git (so there is a permanent, dated record of every decision), and each phase ends at a **[gate](../glossary.md#gate)** — a checkpoint where the work waits for approval before continuing.

| Phase | Name | Done by | Written record (in Git) | Gate |
|---|---|---|---|---|
| 0 | Inception | Human + Architect agent | `constitution.md` — the project's rulebook | Human approves it once; changed only via pull request afterward |
| 1 | Intake & spec | Analyst [agent](../glossary.md#agent) (a conversation with you) | `specs/<feature>/spec.md` — what to build, in testable statements | Spec approval (depends on risk tier, §3) |
| 2 | Architecture | Architect agent | `specs/<feature>/design.md` + `docs/adr/NNN-*.md` — how to build it, with alternatives considered | Design approval (risk-tiered) |
| 3 | Task decomposition | Planner agent | GitHub [Issues](../glossary.md#issue) — the work broken into small, ordered, testable tasks | Optional human skim |
| 4 | TDD build loop | Test Engineer + Coder agents | A [branch](../glossary.md#branch) per task; a commit with failing tests → a commit that makes them pass → cleanup | Pull request opened |
| 5 | Review & triage | AI reviewer(s) + human reviewer + Arbiter | Review comments + triage classifications | Merge approval (risk-tiered) |
| 6 | Merge & retrospective | Automated checks + Retro agent | Protected-branch merge; `retros/<feature>.md` | [Branch protection](../glossary.md#branch-protection) — a GitHub setting that physically blocks merging until required checks pass |

Feedback loop: when a review critique is accepted in Phase 5, the task goes back to Phase 4 on the same branch. Going around the loop more than once is the normal path, not a failure.

> **Software Engineering Validation:** This is a standard SDLC phase-gate model with artifacts-as-code. Specs are BDD-style acceptance criteria, architecture decisions land as ADRs, Phase 4 is strict TDD (red → green → refactor, enforced mechanically — see playbook §4), and every gate is a PR approval backed by branch protection with required status checks. Nothing here is novel process; what's novel is that agents execute it and the enforcement is mechanical rather than cultural.

## 2. Constitution (Phase 0)

`constitution.md` is the project's rulebook — the engineering rules that are not up for debate mid-project. Every agent reads it at the start of every task. The default rules:

- **Tests come first, always.** No product code may be written before a failing test exists that the code must satisfy. This is [TDD](../glossary.md#tdd-test-driven-development) — test-driven development — and it is enforced by machinery, not honor (playbook §4).
- **Minimum test [coverage](../glossary.md#coverage):** 80% of all lines, 90% of the lines changed in any pull request, checked automatically.
- **Every requirement must be phrased testably**, in [Given/When/Then](../glossary.md#givenwhenthen) form ("Given a logged-out visitor, When they submit a valid email, Then an account is created").
- **Significant technical decisions get a written record** — an [ADR](../glossary.md#adr-architecture-decision-record) (architecture decision record) listing the alternatives that were considered and why they lost.
- **Risk-tier definitions and gate policy** (§3 below) — each project tunes these here.
- **An uncertain or blocked agent asks, never guesses:** it opens a `needs-human` issue and stops.
- **Humans may veto at any gate at any time.** The tiers below only set which gates *require* a human; nothing stops you from stepping in anywhere.

## 3. Risk-tiered gates

Not every change deserves the same level of scrutiny: fixing a typo in the documentation is not the same as changing how the software handles passwords. So AIDSEF sorts every change into a **[risk tier](../glossary.md#risk-tier)** — a label that says how careful everyone (human and AI) has to be with it — and the tier decides which checkpoints require a human.

### 3.1 Change classes

First, what *kind* of work is it? There are four classes:

- **Feature** — building something new. Goes through the full lifecycle (Phases 1–6).
- **Fix** — repairing something broken. Abbreviated path: report the problem → write a test that reproduces the bug (so it can never sneak back) → fix it → review → merge. No new spec is written; the fix links back to the spec it corrects.
- **Chore** — housekeeping: updating [dependencies](../glossary.md#dependency) (the third-party code your project builds on), documentation, or tooling. Skips Phases 1–3.
- **[Spike](../glossary.md#spike)** — a sanctioned throwaway experiment. Sometimes the fastest way to answer "would this even work?" is to just try it, with no specs and no tests. Spikes make that legitimate *inside* the framework instead of a workaround: they live on branches named `spike/…`, skip every checkpoint — and in exchange can never merge into the real codebase (the automated checks physically refuse any pull request from a spike branch). What the spike taught you gets written down; anything worth keeping is rebuilt properly through the normal lifecycle. Spikes carry no risk tier, because the tier system exists to govern what merges — and spikes don't.

### 3.2 Risk tiers (defaults; adjust yours in the constitution)

| Tier | What lands a change here (any one trigger is enough) |
|---|---|
| **High** | Anything touching logins or permissions; payments or money movement; personal data or changes to how data is stored; the software's public-facing connection points that other systems depend on; security or server configuration; adding a new third-party dependency; or any change over 400 lines of code |
| **Standard** | Ordinary feature or fix work that doesn't match High or Low |
| **Low** | Documentation, adding tests without touching product code, formatting, or small mechanical cleanups under 50 lines that leave all test results unchanged |

### 3.3 What each tier requires at each gate

| Gate | High | Standard | Low |
|---|---|---|---|
| Spec approval | Human required (work stops until you approve) | Human required (approvals can be batched at your convenience) | Not applicable / AI approves, human notified |
| Design approval | Human required (blocking) | AI reviews its own design; you're notified and have one business day to object | Skipped |
| Merge approval | Human approval + AI review + all automated checks green | AI review + green checks; humans spot-check a sample after merge | AI review + green checks |

The Planner agent proposes each item's risk tier and stamps it on the work item as a [label](../glossary.md#label). **You can overrule it with one click** — change the label, and the tier changes. Raising anything to High immediately re-arms every human checkpoint for it.

> **Software Engineering Validation:** Conventional change-management risk classification mapped onto phase-gate governance. Triggers for High are the usual suspects — auth/authz, payments, PII and schema migrations, public API contracts, security/infra config, new third-party dependencies, >400 changed LOC. Tier assignment is Planner-proposed and human-overridable via a single label change; re-tiering to High re-arms all human gates for that item. Gate enforcement is mechanical where GitHub allows it — branch protection with required status checks — not procedural. Tune the triggers per-project in `constitution.md`. The Spike class is XP's "spike solution" made mechanical: exploration code is unreviewable by design, so a CI guard on `spike/*` head branches bars it from `main` outright — the explicit prototype/production boundary that keeps prototypes from shipping by accident.

## 4. Operating profiles

Same process whether you work alone or in a team — only *who approves what* changes. The profile is declared in `constitution.md`.

### Solo profile
One human wears all the hats. Gates show up as GitHub approval requests and VS Code notifications. Your daily loop: approve specs, skim designs, review high-risk pull requests, and overrule the AI's triage calls whenever you disagree.

### Team profile
| Gate | Approver of record |
|---|---|
| Spec | Product owner |
| Design | Senior/staff engineer (or architect) |
| Merge (High) | Senior engineer + AI review |
| Constitution amendments | Engineering lead |

> **Software Engineering Validation:** This is standard phase-gate + code-review governance with an ordinary RACI split. AIDSEF changes *who does the labor* (AI), not *who holds authority* (humans, via the same PR approvals they use today).

## 5. Review & triage protocol (summary — detail in playbook §4)

Every review critique — whether raised by an AI reviewer or a human — is classified by the Arbiter agent, which must post its reasoning alongside each call:

- `blocking` — the merge is barred until this is addressed
- `fix-now` — worth fixing immediately; the task returns to Phase 4
- `deferred` — a real issue, but not now; automatically filed as a backlog issue that links back to the pull request
- `rejected` — the cost of fixing exceeds the benefit; the reasoning is recorded on the pull request

**Human reviewers outrank the Arbiter:** a human reply reclassifies any item, no ceremony required.

## 6. Retrospective loop (lightweight, v1)

After each completed feature (not each task), the Retro agent looks back at how the work actually went:

1. It mines the feature's history: which review findings recurred, what the automated checks caught, which commits had to be undone, and where humans overrode the AI's triage calls.
2. It writes `retros/<feature>.md` — what recurred, what escaped, what the humans overrode and why.
3. When it spots an actionable pattern, it opens a pull request proposing a change to `constitution.md` or an agent's charter.

Amendment pull requests are **always human-approved**. The framework improves itself under the same governance it applies to code.

> **Software Engineering Validation:** Data-driven agile retrospectives with the output constrained to auditable artifacts: every process change arrives as a human-approved PR against the constitution or a role charter, never as silent drift.
