# 004. Framework-development ADRs live in the framework folder; `project/adr/` ships README-only

- Status: proposed
- Date: 2026-07-20
- Feature: project-workspace

## Context

The migration must place the repository's Architecture Decision Records somewhere.
Two forces pull in different directions:

- **AC-016** requires that when a clone writes its first ADR, it is numbered
  **001** — and states that the framework's own ADR-001 (the DGX Spark / Qwen model
  decision) **moves into `aidsef-framework-development-content/`** and that
  `project/adr/` **ships with only a README**. The motivating defect (spec
  "Evidence"): dogfood project #1 inherited the framework's ADR-001 as its own
  first decision record, which is nonsense for that project.
- **Resolved question Q2** keeps the template honest by dogfooding: the template's
  own work products — its specs, its retros — live under `project/` like any
  clone's, and the trim step empties `project/` contents (keeping the READMEs).

Read together these create a question the spec does not answer directly: **where do
the ADRs this very feature produces (ADR-002, ADR-003, ADR-004) go?** If they were
treated like specs/retros and left in `project/adr/`, then `project/adr/` would
*not* "ship with only a README" (AC-016) until a clone runs the trim — and a clone
that trimmed in the wrong order, or inspected before trimming, would again inherit
a stray ADR-001…00N as its first decisions. AC-016's guarantee is stronger than
"emptied on trim"; it says the shipped state of `project/adr/` is README-only.

There are therefore two kinds of ADR in play:

- **Framework-development ADRs** — decisions about how AIDSEF *itself* is built:
  ADR-001 (the local model plane) and this feature's ADR-002/003/004 (how the
  template was restructured). This is framework-authoring knowledge that must *not*
  travel to clones.
- **A clone's project ADRs** — the decision records a downstream project writes for
  its own product. These belong in `project/adr/`, starting fresh at 001.

## Decision

**All framework-development ADRs live in `aidsef-framework-development-content/adr/`.
`project/adr/` ships containing only its `README.md`.**

- The build `git mv`s `docs/adr/001-local-model-qwen36-35b-a3b.md` and this
  feature's `docs/adr/002-*`, `003-*`, `004-*` into
  `aidsef-framework-development-content/adr/`, alongside the playbook and
  build-order doc that already reference ADR-001.
- `project/adr/README.md` (the relocated, updated `docs/adr/README.md`) is the only
  file under `project/adr/` in a fresh clone. It tells a project its first ADR is
  `001-<slug>.md`.
- Because framework ADRs sit inside `aidsef-framework-development-content/`, the
  two-step trim (AC-015) removes them wholesale when a clone deletes that folder —
  no per-ADR keep/delete decision, and no risk of a clone inheriting framework
  decisions.

This treats ADRs differently from specs/retros on purpose. Specs and retros stay
under `project/` (Q2) because they are living demonstrations of the lifecycle a
clone will run, and a stray *spec* folder is self-evidently the template's own. An
ADR is different: it is numbered, and a numbered `project/adr/001` is precisely the
artifact AC-016 exists to prevent a clone from inheriting. The stronger "ships
README-only" guarantee is worth the small asymmetry.

## Alternatives considered

- **Leave this feature's ADRs in `project/adr/` and rely on the trim to empty
  them.** Rejected: it violates AC-016's shipped-state guarantee ("`project/adr/`
  ships with only a README"), and reintroduces the exact inheritance bug — a clone
  inspecting or partially trimming would find `project/adr/002-…` and read it as its
  own. It also splits framework-development ADRs across two folders (ADR-001 in the
  framework folder, ADR-002+ under `project/`), which is incoherent.
- **Move only ADR-001 to the framework folder (literal reading of AC-016) and put
  ADR-002/003/004 under `project/adr/`.** Rejected for the same shipped-state and
  inheritance reasons; AC-016 names ADR-001 because that is the ADR that exists
  today, not because it is the only framework ADR. The principle it encodes —
  clones start their ADR numbering at 001 — applies to every framework-development
  ADR.
- **Keep every ADR in `docs/adr/` and never introduce `project/adr/`.** Rejected:
  the target-layout table assigns the project's decision records to `project/adr/`,
  and a clone writing to `docs/adr/` would collide with the framework's own ADRs and
  re-inherit ADR-001.

## Consequences

- **Easier:** a fresh clone's `project/adr/` is unambiguously empty-but-documented;
  its first ADR is 001; the trim removes all framework ADRs in one folder delete;
  framework-development decisions stay together with the playbook that cites them.
- **Harder / watch for:** this feature's own ADRs (002–004) end up in a *different*
  tree from its spec and design (`project/specs/project-workspace/`), so the
  project-workspace feature's artifacts are deliberately split — framework-authoring
  ADRs in the framework folder, the dogfood spec/design under `project/`. The design
  documents this split so a reader is not surprised to find the design referencing
  ADRs that live elsewhere. Future framework-development work continues numbering in
  `aidsef-framework-development-content/adr/` (next is 005); a clone's project ADRs
  are an independent 001-based sequence.
