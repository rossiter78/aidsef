---
name: aidsef-plan
description: Phase 3 of the AIDSEF lifecycle — break an approved design into small, ordered GitHub Issues with acceptance-criteria references and proposed risk-tier labels.
argument-hint: [feature-name]
disable-model-invocation: true
---

# /aidsef-plan — task decomposition (Phase 3)

Delegate this phase to the **planner** subagent (charter: `.claude/agents/planner.md`); it must read `constitution.md` first. Feature: `$ARGUMENTS` — if empty, ask.

## Preconditions

- The design gate passed: `specs/<feature>/design.md` is merged (High: approved; Standard: objection window elapsed or human waved it through).

## Steps

1. **Spawn the planner** with the spec, design, and constitution. For each task it defines, it opens a GitHub Issue via `gh issue create` using the task issue template, containing:
   - Which `AC-*` criteria the task covers (every criterion in the spec must be covered by at least one task — say which)
   - What "done" means for the task
   - Proposed `risk:high|standard|low` label with one line of reasoning
   - Dependency notes (`Blocked by #NN`) and a milestone or `feature:<name>` label tying the tasks together
2. **Order the queue**: apply the `ready` label to tasks whose dependencies are already met; leave the rest unlabeled until unblocked.
3. **Report to the human** (the optional Phase 3 skim): list the issues with tiers and order, flag anything tiered `risk:high`, and remind them one label click re-tiers any task (constitution §3).

## Rules

- Right-size for the local Coder: one task ≈ one branch ≈ one PR, ideally under ~200 changed lines. Escalation diagnoses of "task badly specified" land on the Planner in retros.
- The Planner merges and approves nothing, and never downgrades a human-set risk label.
- Blocked or uncertain → `needs-human` issue; never guess.
