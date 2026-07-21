# Specs

One folder per feature: `specs/<feature>/`.

- `spec.md` — what to build, in numbered Given/When/Then acceptance criteria (`AC-001`, …). Written by the **Analyst** in Phase 1 (`/aidsef-spec`).
- `design.md` — how to build it, mapping every criterion to a component. Written by the **Architect** in Phase 2 (`/aidsef-design`).

Both land by pull request at a human-reviewable gate. Decision records for a feature go in [`docs/adr/`](../docs/adr/); the generated requirement→test tables go in [`docs/traceability/`](../docs/traceability/).
