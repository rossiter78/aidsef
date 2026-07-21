# Spec: project-workspace

- Status: **draft** — Phase 1, under review in chat
- Feature: `project-workspace`
- Analyst session: 2026-07-20
- Proposed risk tier: **`risk:high`** — modifies the enforcement machinery itself (skills, workflows, traceability tool), far exceeds 400 changed lines, and touches `constitution.md`; per constitution §8 these are human-approved amendments regardless of tier.

## Summary

When someone clones the AIDSEF template to start their own project, three things are unclear: which files belong to the framework versus their project, where to put planning documents they have already written, and where the documents AIDSEF's agents will create are going to land. This feature draws that boundary structurally: everything the project owns lives under one directory (`project/`), pre-existing documents get a designated intake spot (`project/inputs/`) that the lifecycle reads by default, framework-only material is consolidated so a new project can remove it in one step, and the slash commands are renamed so their phase order is visible in the command menu.

**Evidence** (dogfood project #1, `ai-readiness-assessment`): prior analysis got parked in an improvised `docs/assessment/` folder because no designated place existed; the framework's own ADR-001 (a decision about AIDSEF's inference host) was inherited as the project's first decision record; and when running `/aidsef-spec`, the human could not predict what it would do or where its output would be stored.

## Sources

*(This section is itself the provenance convention that AC-007 mandates.)*

- The Analyst interview in chat, 2026-07-20 (all requirements confirmed by the human)
- Reference inventory of the template repo: 17 references to `specs/`, 11 to `docs/adr/`, 4 to `docs/traceability/`, 6 to `retros/`
- Inspection of dogfood project #1 (`ai-readiness-assessment`): `docs/assessment/` (14 documents), `TechnicalPlan.md`, `ROADMAP.md`, inherited `docs/adr/001-*`

## Target layout

| Path | Who writes there | What it holds |
|---|---|---|
| `project/` | **The cloning project** | Everything the project owns — one boundary, one rule |
| `project/inputs/` | The human | Pre-existing material: prior specs, plans, designs, research |
| `project/specs/<feature>/` | Analyst (Phase 1), Architect (Phase 2) | `spec.md`, `design.md` |
| `project/adr/` | Architect | The project's decision records, starting at 001 |
| `project/traceability/` | CI (generated) | Requirement→test tables |
| `project/retros/` | Retro agent (Phase 6) | Per-feature retrospectives |
| `docs/` | Framework (ships with clones) | The AIDSEF manual: glossary, user-facing guides |
| `aidsef-framework-development-content/` (root) | Framework authors only | Material that does **not** travel to clones: playbook 01–06, the build-order doc, framework ADRs, the framework's deferred-ideas list |
| `constitution.md` | Root — unchanged | Human decision: visibility outranks tidiness |

## Acceptance criteria

### A. Workspace structure

- **AC-001** — Given a fresh clone of the template, When the user lists the repository root, Then a `project/` directory exists containing `inputs/`, `specs/`, `adr/`, `traceability/`, and `retros/`, each holding a `README.md` that states in plain language who writes there and during which lifecycle phase.
- **AC-002** — Given the completed migration, When the repository is searched for references to the old artifact paths (root `specs/`, `docs/adr/`, `docs/traceability/`, root `retros/`), Then no reference remains in any tracked file.
- **AC-003** — Given the new layout, When `tools/check_traceability.py` runs, Then it reads specs from `project/specs/*/spec.md`, writes matrices to `project/traceability/`, and the existing test suite passes against the new paths.
- **AC-004** — Given the new layout, When the `ci` workflow runs, Then the traceability artifact uploads from `project/traceability/`, and the `claude-review` workflow prompt points reviewers at `project/specs/` and `project/adr/`.
- **AC-005** — Given the new layout, When any role charter or skill is read, Then every path it names (specs, ADRs, traceability, retros, inputs) is a `project/…` path.

### B. Inputs and absorption

- **AC-006** — Given a fresh clone, When the user opens `project/inputs/README.md`, Then it explains: put pre-existing documents here; agents read them during spec and design; specs cite what they used; and once a spec covering the material merges, **the spec governs** and the input remains as an unmodified historical record.
- **AC-007** — Given documents exist in `project/inputs/`, When `/aidsef-1-spec` runs, Then the skill directs the Analyst to read `project/inputs/` before interviewing, and the produced `spec.md` contains a **Sources** section listing each input document used (or stating that none existed).
- **AC-008** — Given documents exist in `project/inputs/`, When `/aidsef-2-design` runs, Then the skill directs the Architect to read `project/inputs/`, and the produced `design.md` cites the input documents it drew on in a Sources section.
- **AC-009** — Given a merged spec and an input document that disagree, When any agent consults them, Then the rule "the merged spec wins; inputs are historical once absorbed" is stated in `project/inputs/README.md` and in the Analyst and Architect charters.

### C. Skill renames

- **AC-010** — Given the renamed skills, When the user opens the slash-command menu, Then the lifecycle commands read `aidsef-1-spec`, `aidsef-2-design`, `aidsef-3-plan`, `aidsef-4-build`, `aidsef-6-retro`, and invoking each runs the corresponding phase.
- **AC-011** — Given the completed rename, When the repository is searched for the old skill names (`aidsef-spec`, `aidsef-design`, `aidsef-plan`, `aidsef-build`, `aidsef-retro` as command references), Then no reference remains in any tracked file.
- **AC-012** — Given the numbering gap, When the user reads the README or the clone-facing guide, Then it states in one sentence that Phase 5 (review) has no command because it runs automatically on every pull request.

### D. Documentation

- **AC-013** — Given a fresh clone, When the user reads the clone-facing guide, Then it contains a table mapping each lifecycle phase → the command to type (or "automatic") → where the output lands.
- **AC-014** — Given a user with pre-existing documents, When they read the clone-facing guide, Then it tells them: put existing documents in `project/inputs/`, what the agents will do with them (absorption with cited sources), and where the resulting source-of-truth documents will live (`project/specs/`).
- **AC-015** — Given the consolidated framework-authoring folder, When a new project trims the template, Then the instruction is exactly two mechanical steps — delete `aidsef-framework-development-content/`, and empty the contents of `project/` subfolders (keeping their READMEs) — replacing today's multi-item keep/delete checklist.
- **AC-016** — Given the migration, When a clone writes its first ADR, Then it is numbered 001 — the framework's ADR-001 (DGX Spark) has moved into `aidsef-framework-development-content/` and `project/adr/` ships with only a README.
- **AC-017** — Given a fresh clone, When the user opens the root `BACKLOG.md`, Then it is an empty, ready-to-use list — the framework's own deferred ideas have moved into `aidsef-framework-development-content/`.

## Out of scope

- Migrating dogfood project #1 (`ai-readiness-assessment`) to the new layout — separate task in that repo.
- Authoring a full "how to run your project" playbook series — the clone-facing guide covers usage; anything more goes to `BACKLOG.md`.
- Any tooling that automatically modifies or stamps input documents — absorption is recorded in specs, never written onto inputs.
- Changes to lifecycle phases, gates, risk tiers, quality thresholds, or any governance rule.
- The `resident-*` workflows and LiteLLM configuration.

## Resolved questions

All three open questions were resolved with the human in the Analyst session (2026-07-20):

- **Q1** — Framework-authoring folder is **`aidsef-framework-development-content/`** at the repository root (human's choice: maximum clarity over brevity).
- **Q2** — The template's own work products (its specs, retros) live in `project/` like any project's; the trim step **empties `project/` contents** (READMEs stay). Dogfooding stays honest; agents execute the trim.
- **Q3** — Framework's deferred ideas move into `aidsef-framework-development-content/`; root `BACKLOG.md` **ships empty**.
