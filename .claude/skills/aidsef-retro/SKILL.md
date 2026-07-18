---
name: aidsef-retro
description: Phase 6 of the AIDSEF lifecycle — after a feature completes, mine its history into retros/<feature>.md and, when patterns warrant, propose constitution or charter amendments as human-approved pull requests.
argument-hint: [feature-name]
disable-model-invocation: true
---

# /aidsef-retro — retrospective (Phase 6)

Delegate this phase to the **retro** subagent (charter: `.claude/agents/retro.md`); it must read `constitution.md` first. Feature: `$ARGUMENTS` — if empty, ask.

Run once per completed **feature**, not per task.

## Steps

1. **Mine the history** via `gh` and `git log` for every task in the feature:
   - Review findings by category, and how the Arbiter classified each
   - Triage calls a human overrode, and what they said
   - Escalation requests: count, diagnosis given, outcome (`escalate` vs `re-scope`)
   - Red-proof failures, reverted commits, review cycles per PR
   - Coverage delta and (for `risk:high` work) mutation scores
2. **Write `retros/<feature>.md`** on branch `retro/<feature>`: what recurred, what escaped to a human, what humans overrode and why, and the numbers. Plain language — the human approving amendments is the audience.
3. **Open the retro PR** (`Retro: <feature>`, `risk:low`).
4. **Propose amendments only when the evidence says so**: a pattern needs at least two occurrences. Each proposal is its **own separate PR** against `constitution.md` or one charter, citing the retro. Amendment PRs are **always human-approved** (constitution §8) — say so in the PR body and never merge them yourself.
5. **Report**: summarize the retro in chat, list any amendment PRs opened, and — if the trust milestones in constitution §6 are met — note that the human may want to consider moving the autonomy dial (their call, via amendment).

## Rules

- Evidence first: no amendment proposal without the retro data behind it.
- Watch escalation telemetry both directions: constant escalation questions the local model's slot; repeated "badly specified" diagnoses question the Planner.
- The Retro agent never rewrites history or edits past retros.
