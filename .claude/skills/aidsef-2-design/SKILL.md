---
name: aidsef-2-design
description: Phase 2 of the AIDSEF lifecycle. Reads the approved specs/<feature>/spec.md and project/inputs/. Produces specs/<feature>/design.md (with a Sources section) plus any ADRs in docs/adr/, proposed as a pull request for the design-approval gate.
argument-hint: [feature-name]
disable-model-invocation: true
---

# /aidsef-2-design — architecture (Phase 2)

Delegate this phase to the **architect** subagent (charter: `.claude/agents/architect.md`); it must read `constitution.md` first. Feature: `$ARGUMENTS` — if empty, ask.

## Preconditions

- `specs/<feature>/spec.md` exists on `main` (its PR was approved and merged). If the spec PR is still open, stop and tell the human which gate is pending.

## Steps

1. **Spawn the architect** with the approved spec, the constitution, `project/inputs/` (the pre-existing material the spec drew on), and the current codebase. It produces, on branch `design/<feature>`:
   - `specs/<feature>/design.md` — components, data flow, interfaces, error handling, a mapping of every `AC-*` to the component(s) that satisfy it, and a **Sources** section citing the `project/inputs/` documents it drew on (or noting none existed)
   - `docs/adr/NNN-<slug>.md` for each significant decision: context, decision, alternatives considered, why they lost. Number sequentially from the highest existing ADR.
2. **Check the hard limits held**: no implementation code in the diff; every acceptance criterion mapped; any new third-party dependency has its own ADR **and** re-tiers the feature to `risk:high` (constitution §3.2).
3. **Open the gate PR**: `gh pr create` titled `Design: <feature>`, body listing the ADRs and the AC coverage map; apply the feature's `risk:*` label.
4. **Run the gate per constitution §3.3**:
   - **High** — human approval, blocking. Announce and stop.
   - **Standard** — AI design self-review: spawn a fresh architect-charter subagent to critique the design against the spec; post the critique as a PR comment; notify the human they have one business day to object before it proceeds.
   - **Low** — skipped (design phase itself is normally skipped for Low; note why if you got here).

## Rules

- The Architect never weakens a criterion to make the design easier — unbuildable criteria go back via `needs-human`.
- Blocked or uncertain → `needs-human` issue; never guess.
