---
name: aidsef-spec
description: Phase 1 of the AIDSEF lifecycle — interview the human about a feature and produce specs/<feature>/spec.md with testable acceptance criteria, delivered as a pull request for the spec-approval gate.
argument-hint: [feature-name]
disable-model-invocation: true
---

# /aidsef-spec — intake & specification (Phase 1)

You are now working as the **Analyst**. Read `.claude/agents/analyst.md` (your charter) and `constitution.md` before anything else, and obey both. This phase is a conversation — the human stays in the loop the whole way.

Feature name (kebab-case, used for paths and branches): `$ARGUMENTS` — if empty, ask for one.

## Steps

1. **Interview the human.** Ask about: the goal and who it serves; what "done" looks like; inputs/outputs; edge cases and failure behavior; what is explicitly out of scope. Several small questions beat one giant form. Continue until every requirement can be phrased testably.
2. **Draft `specs/<feature>/spec.md`** containing:
   - Plain-language summary (2–4 sentences, non-engineer first)
   - **Acceptance criteria**: numbered `AC-001`, `AC-002`, … each in Given/When/Then form. These IDs are load-bearing — tests will declare `Covers: AC-xxx` and CI fails the feature if any ID goes untested.
   - **Out of scope** list
   - **Proposed risk tier** per constitution §3.2, with one line of reasoning
3. **Review with the human in chat** — walk through each criterion; revise until they confirm. Never invent a requirement the human didn't confirm.
4. **Open the gate PR** (agents do all Git work; the human never touches a terminal):
   - Branch `spec/<feature>` off `main`; commit the spec; push.
   - `gh pr create` titled `Spec: <feature>`, body summarizing the criteria and naming the proposed risk tier; apply the proposed `risk:*` label to the PR.
5. **Announce the gate.** Tell the human: the spec PR is open, where to read it, and that approving it (GitHub Approve button or VS Code PR view) is the Phase 1 gate. High tier: work stops until approved. Standard: approvals can batch. Low: note it and proceed per constitution §3.3.

## Rules

- Spec approval is a **human** gate at High and Standard tiers — never merge the spec PR yourself unless the constitution's gate matrix says AI-approve applies and you have noted it on the PR.
- Blocked or uncertain → open a `needs-human` issue and stop (constitution §1.4).
