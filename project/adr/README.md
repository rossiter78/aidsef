# Architecture Decision Records

One file per significant technical decision: `NNN-<slug>.md`, numbered sequentially — a project's decision records start at `001`. An [ADR](../../docs/glossary.md#adr-architecture-decision-record) records **what was decided, what alternatives were considered, and why they lost** — so anyone can later ask "why is it built this way?" and get a real answer.

The **Architect** writes these in Phase 2. A decision is "significant" when it is hard to reverse, adds a [dependency](../../docs/glossary.md#dependency) (which also re-tiers the change to `risk:high`), or shapes how later work must be built.

Suggested shape:

```markdown
# NNN. <title>

- Status: proposed | accepted | superseded by ADR-XXX
- Date: YYYY-MM-DD
- Feature: <feature>

## Context
What forces are at play — the problem, constraints, requirements.

## Decision
What we chose to do.

## Alternatives considered
Each option weighed, and why it lost.

## Consequences
What becomes easier or harder as a result.
```
