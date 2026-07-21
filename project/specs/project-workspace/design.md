# Design: project-workspace

- Status: **proposed** — Phase 2, design-approval gate (High tier, human-approved)
- Feature: `project-workspace`
- Spec: [`spec.md`](spec.md) (approved, merged — PR #20)
- Architect session: 2026-07-20
- ADRs: [002 (git mv history)](../../docs/adr/002-preserve-history-with-git-mv.md) ·
  [003 (numbered skill names)](../../docs/adr/003-numbered-skill-command-names.md) ·
  [004 (framework-ADR location)](../../docs/adr/004-framework-development-adrs-location.md)

> **Note on this file's own paths.** This design is written in the *current,
> pre-migration* layout, so its links point at `../../docs/adr/…`. The feature it
> designs will `git mv` this very file to `project/specs/project-workspace/design.md`
> and move the ADRs into `aidsef-framework-development-content/adr/`; the reference
> sweep (§9) fixes these links as part of the build. See §8 (recursion) for why the
> design describing the migration is itself migrated by it.

## 1. Overview

This is a **structural refactor of the template repository**, not a code feature.
It ships no `src/**` product code. The work is: (a) relocate every project-owned
artifact directory under a single `project/` boundary; (b) consolidate every
framework-authoring file that must *not* travel to clones into one deletable
folder, `aidsef-framework-development-content/`; (c) add an intake folder
`project/inputs/` that the lifecycle reads by default; (d) rename the five phase
skills so the slash-command menu reads in lifecycle order; and (e) sweep every
tracked file so no reference points at an old path or old command name.

Because AIDSEF **dogfoods itself**, the template's own work products are treated
exactly like a clone's: this feature's spec and design live under `project/specs/`
after the migration (§8). The design is therefore self-referential and must be
internally consistent about that — it is.

### 1.1 Design principles carried from the spec

- **One boundary, one rule** (spec summary): everything the project owns is under
  `project/`; everything framework-only is under
  `aidsef-framework-development-content/`; the two-step trim (AC-015) is only
  possible because those two folders partition the movable surface cleanly.
- **No behavioral change to governance.** Gates, tiers, thresholds, the red proof,
  and the traceability *rules* are untouched (spec "Out of scope"). Only the
  *paths* those mechanisms read/write change.
- **History is evidence.** Moves preserve `git blame`/`--follow` lineage
  ([ADR-002](../../docs/adr/002-preserve-history-with-git-mv.md)).

## 2. Components affected (data flow)

The lifecycle's data flow is unchanged; only the read/write locations move. The
components that carry a hard-coded path (and therefore change) are:

| Component | Reads | Writes | Path change |
|---|---|---|---|
| `tools/check_traceability.py` | `project/specs/*/spec.md`, `tests/**` | `project/traceability/` | `SPEC_GLOB`, `OUT_DIR` (AC-003) |
| `ci.yml` traceability step | (runs the tool) | uploads `project/traceability/` artifact | upload `path:` (AC-004) |
| `claude-review.yml` prompt | points reviewers at `project/specs/`, `project/adr/` | — | prompt text (AC-004) |
| Analyst (`aidsef-1-spec` + charter) | `project/inputs/`, `project/specs/` | `project/specs/<f>/spec.md` (+ Sources) | reads/writes + inputs direction (AC-005/006/007/009) |
| Architect (`aidsef-2-design` + charter) | `project/inputs/`, `project/specs/`, `project/adr/` | `project/specs/<f>/design.md` (+ Sources) | reads/writes + inputs direction (AC-005/008/009) |
| Planner / Coder / Test-Eng / Reviewer / Retro charters & skills | `project/specs/`, `project/adr/`, `project/retros/` | `project/retros/` (Retro) | path sweep (AC-005) |

`tests/**` and any future `src/**` stay at the repository root — they are the
cloning project's *code*, not lifecycle artifacts, and are outside the `project/`
artifact boundary. Only the tool's `TESTS_DIR` scan target is therefore left
unchanged.

## 3. Migration map (every file's disposition)

The build executes this table. Per [ADR-002](../../docs/adr/002-preserve-history-with-git-mv.md),
**moves are `git mv` committed first, edits follow in separate commits.**

### 3.1 Project-owned artifacts → `project/`

| From | To | Then edit for |
|---|---|---|
| `specs/` (dir) | `project/specs/` | — |
| `specs/README.md` | `project/specs/README.md` | AC-001 wording; new command names; fix `../docs/adr/`→`../adr/`, `../docs/traceability/`→`../traceability/` |
| `specs/project-workspace/spec.md` | `project/specs/project-workspace/spec.md` | sweep allowlist entry (§8, §9) |
| `specs/project-workspace/design.md` (this file) | `project/specs/project-workspace/design.md` | fix ADR links → `../../aidsef-framework-development-content/adr/…`; sweep allowlist entry |
| `docs/traceability/` (dir) | `project/traceability/` | — |
| `docs/traceability/README.md` | `project/traceability/README.md` | AC-001 wording; tool link still `../../tools/check_traceability.py` (depth unchanged) |
| `retros/` (dir) | `project/retros/` | — |
| `retros/README.md` | `project/retros/README.md` | AC-001 wording; `/aidsef-retro`→`/aidsef-6-retro`; fix `../constitution.md`→`../../constitution.md` |
| `docs/adr/README.md` | `project/adr/README.md` | AC-001 wording (a project's ADRs start at 001); fix `../glossary.md`→`../../docs/glossary.md` |

Result: `project/adr/` contains **only** `README.md` (AC-016) — the ADR *files* go
to the framework folder (§3.3).

### 3.2 New project folder

| Create | Content |
|---|---|
| `project/inputs/README.md` | AC-006 + AC-009 content (see §6) |

### 3.3 Framework-only material → `aidsef-framework-development-content/`

| From | To |
|---|---|
| `docs/adr/001-local-model-qwen36-35b-a3b.md` | `aidsef-framework-development-content/adr/001-…` (AC-016) |
| `docs/adr/002-preserve-history-with-git-mv.md` | `aidsef-framework-development-content/adr/002-…` ([ADR-004](../../docs/adr/004-framework-development-adrs-location.md)) |
| `docs/adr/003-numbered-skill-command-names.md` | `aidsef-framework-development-content/adr/003-…` |
| `docs/adr/004-framework-development-adrs-location.md` | `aidsef-framework-development-content/adr/004-…` |
| `docs/playbook/` (01–06) | `aidsef-framework-development-content/playbook/` |
| `docs/00-getting-started.md` | `aidsef-framework-development-content/00-getting-started.md` (framework build-order record; its Phase D onboarding becomes a pointer to the new clone-facing guide — see §7) |
| `BACKLOG.md` (content) | `aidsef-framework-development-content/BACKLOG.md` (AC-017) |

After the move, the framework folder holds: `adr/` (001–004), `playbook/`,
`00-getting-started.md`, `BACKLOG.md`. Deleting this one folder removes all
framework-authoring material (AC-015).

### 3.4 Replace-in-place (new content, not a move)

| File | New content |
|---|---|
| `BACKLOG.md` (root) | empty, ready-to-use list — heading + one line of guidance, no items (AC-017) |
| `docs/00-getting-started.md` (root) | the **clone-facing guide** (§7) — AC-012/013/014/015 |

### 3.5 Machinery & config edits (stay in place; content sweep only)

`tools/check_traceability.py` (§4) · `.github/workflows/ci.yml` (§4) ·
`.github/workflows/claude-review.yml` (§5) · `.github/workflows/resident-build.yml`
(command-name string only — §9.3) · `.github/ISSUE_TEMPLATE/task.yml` ·
`constitution.md` (§1.3 `docs/adr/`→`project/adr/`; playbook links — §9.4) ·
`CLAUDE.md` · `README.md` · `docs/glossary.md` · `.claude/agents/*.md` (9 charters +
README) · `.claude/skills/*` (renamed — §5) · `tests/test_check_traceability.py` ·
`tests/test_traceability_enforcement.py` (§4).

## 4. Traceability tool + CI (AC-003, AC-004)

### 4.1 `tools/check_traceability.py`

Two module constants change; nothing else in the algorithm does. Interface sketch:

```python
SPEC_GLOB = "project/specs/*/spec.md"   # was "specs/*/spec.md"
TESTS_DIR = Path("tests")               # UNCHANGED — code lives at repo root
OUT_DIR   = Path("project/traceability")# was Path("docs/traceability")
```

The module docstring's path examples (`specs/<feature>/spec.md`,
`docs/traceability/<feature>.md`) are updated to the `project/…` forms in the same
sweep. The `--require-specs` / `--allow-uncovered` semantics are untouched
(governance is out of scope).

### 4.2 Existing tests (AC-003: "the existing test suite passes against the new paths")

`tests/test_check_traceability.py` and `tests/test_traceability_enforcement.py`
build fixtures at `specs/demo` and assert against `docs/traceability`. Both must
move their fixtures to `project/specs/demo` and any output assertion to
`project/traceability`. These are edits to *existing* tests for a path migration;
they modify assertions, which constitution §4 flags for mandatory human review —
already satisfied because this is a High-tier, human-approved PR. At least one test
that exercises the tool reading `project/specs/*` and writing `project/traceability/`
carries a `Covers: AC-003` annotation so AC-003 is mechanically traced.

### 4.3 `ci.yml`

- Upload step `path: docs/traceability/` → `path: project/traceability/` (AC-004).
- The mode-selection logic keys on `^src/` and `^(src|tests)/` — neither moves —
  so it is left unchanged. The tool invocation line is unchanged (the tool now
  finds specs under `project/specs/` internally).

## 5. Reviewer prompt + skills (AC-004, AC-005, AC-007, AC-008, AC-010, AC-011)

### 5.1 `claude-review.yml` prompt (AC-004)

The prompt currently says "the feature's spec and design under `specs/`" and "any
relevant ADRs under `docs/adr/`". Sweep to "under `project/specs/`" and "under
`project/adr/`".

### 5.2 Skill renames (AC-010, AC-011) — see [ADR-003](../../docs/adr/003-numbered-skill-command-names.md)

`git mv` each skill directory (rename = command name):

| From | To | `name:` frontmatter | Command |
|---|---|---|---|
| `.claude/skills/aidsef-spec` | `.claude/skills/aidsef-1-spec` | `aidsef-1-spec` | `/aidsef-1-spec` |
| `.claude/skills/aidsef-design` | `.claude/skills/aidsef-2-design` | `aidsef-2-design` | `/aidsef-2-design` |
| `.claude/skills/aidsef-plan` | `.claude/skills/aidsef-3-plan` | `aidsef-3-plan` | `/aidsef-3-plan` |
| `.claude/skills/aidsef-build` | `.claude/skills/aidsef-4-build` | `aidsef-4-build` | `/aidsef-4-build` |
| `.claude/skills/aidsef-retro` | `.claude/skills/aidsef-6-retro` | `aidsef-6-retro` | `/aidsef-6-retro` |

No Phase-5 skill exists — review runs automatically on every PR (AC-012). Each
skill's `name:` frontmatter and body heading are updated to the new name; the old
directories cease to exist (no alias — ADR-003). Every cross-reference to an old
command in another skill/charter/doc is rewritten to the new name (§9.2).

### 5.3 Analyst & Architect skill "inputs" directions (AC-007, AC-008)

- **`aidsef-1-spec`** — add a step 0 to the Interview: *"Read `project/inputs/`
  first — the human may have placed prior specs, plans, designs, or research there.
  Treat them as background, not gospel."* Add to the "Draft spec.md" step a required
  **Sources** section listing each input document used, **or stating none existed**
  (AC-007).
- **`aidsef-2-design`** — add to the architect's spawn brief: *"Read
  `project/inputs/` for material the spec drew on."* Require a **Sources** section
  in `design.md` citing the input documents drawn on (AC-008). (This design's own
  Sources section, §11, demonstrates the convention.)

### 5.4 Charter path sweep (AC-005)

Every charter under `.claude/agents/` names artifact paths in its Reads/Produces.
All are rewritten to `project/…`:

| Charter | Paths to rewrite |
|---|---|
| `analyst.md` | `specs/`→`project/specs/`; add `project/inputs/` to Reads; Produces Sources; "merged spec wins" (AC-009) |
| `architect.md` | `specs/`→`project/specs/`; `docs/adr/`→`project/adr/`; add `project/inputs/` to Reads; Produces Sources; "merged spec wins" (AC-009) |
| `planner.md` | `specs/`→`project/specs/` |
| `coder.md` | `specs/`→`project/specs/` |
| `test-engineer.md` | `specs/`→`project/specs/` |
| `reviewer.md` | `specs/`→`project/specs/`; `docs/adr/`→`project/adr/` |
| `retro.md` | `retros/`→`project/retros/` |
| charter `description:` frontmatter | old command names → numbered (analyst, architect, planner, coder, test-engineer, retro all name a `/aidsef-*` command) |
| `.claude/agents/README.md` | playbook §2 link (§9.4) |

## 6. `project/inputs/` and absorption (AC-006, AC-009)

`project/inputs/README.md` must state, in plain language:

1. **What goes here** — pre-existing documents: prior specs, plans, designs,
   research (AC-006).
2. **What the agents do with it** — the Analyst reads it before interviewing
   (Phase 1) and the Architect reads it during design (Phase 2); the produced spec
   and design cite what they used in a **Sources** section (AC-006/007/008).
3. **The governing rule** — *once a spec covering the material merges, the merged
   spec governs; the input stays as an unmodified historical record.* If a merged
   spec and an input disagree, **the merged spec wins; inputs are historical once
   absorbed** (AC-006, AC-009).
4. **What never happens** — no agent modifies or stamps an input (spec "Out of
   scope").

The same "merged spec wins; inputs are historical once absorbed" sentence is added
to **`analyst.md`** and **`architect.md`** charters (AC-009) — three statements of
one rule (README + two charters), so whichever surface an agent reads, the rule is
present.

## 7. Clone-facing guide + two-step trim (AC-012, AC-013, AC-014, AC-015)

New `docs/00-getting-started.md` (ships to clones; the framework build-order that
occupied this filename moves to the framework folder, §3.3). It follows the
two-audience pattern (plain language + SEV callouts) and contains:

- **Phase → command → output table** (AC-013), e.g.:

  | Phase | You type | Output lands in |
  |---|---|---|
  | 1 Spec | `/aidsef-1-spec` | `project/specs/<feature>/spec.md` |
  | 2 Design | `/aidsef-2-design` | `project/specs/<feature>/design.md` + `project/adr/` |
  | 3 Plan | `/aidsef-3-plan` | GitHub issues |
  | 4 Build | `/aidsef-4-build <issue>` | `src/**`, `tests/**`, `project/traceability/` |
  | 5 Review | *(automatic on every PR)* | PR review comments |
  | 6 Retro | `/aidsef-6-retro` | `project/retros/<feature>.md` |

  with one sentence stating **Phase 5 has no command because review runs
  automatically on every pull request** (AC-012).

- **Working-with-inputs section** (AC-014): put existing documents in
  `project/inputs/`; the agents absorb them with cited Sources; the resulting
  source-of-truth documents live in `project/specs/`.

- **The two-step trim** (AC-015), replacing the old multi-item keep/delete
  checklist (getting-started Phase D step 4):

  > 1. Delete `aidsef-framework-development-content/`.
  > 2. Empty the contents of each `project/` subfolder, keeping its `README.md`.

  Because §3 partitions the movable surface into exactly those two folders, this is
  complete and mechanical — no per-file judgment.

The moved `aidsef-framework-development-content/00-getting-started.md` keeps Phases
A–C as the framework's historical build record; its Phase D section is reduced to a
pointer at the new clone-facing guide so there is a **single** authoritative trim
instruction (AC-015).

## 8. The `project/` recursion (the template dogfooding itself)

The template dogfoods, so its own work products move under `project/` like any
clone's (Resolved Q2). Concretely:

- `specs/project-workspace/spec.md` → `project/specs/project-workspace/spec.md`
- `specs/project-workspace/design.md` (**this file**) →
  `project/specs/project-workspace/design.md`
- `tools/check_traceability.py` then reads `project/specs/*/spec.md` and writes
  `project/traceability/` — so the very spec that mandated the move is found at its
  new home by the tool the move reconfigured. Consistent.

This feature's **ADRs**, by contrast, go to
`aidsef-framework-development-content/adr/` (not `project/adr/`), because they are
framework-development decisions and `project/adr/` must ship README-only
([ADR-004](../../docs/adr/004-framework-development-adrs-location.md)). So the
project-workspace feature's artifacts are deliberately split: spec+design under
`project/specs/`, ADRs under the framework folder. The design records this so a
reader is not surprised.

**Trim honesty:** after this feature merges, `project/specs/project-workspace/` and
`project/retros/` hold the template's own dogfood artifacts. A clone's trim step 2
empties them (keeping READMEs) — exactly as intended; the template ships them as a
worked example, the clone clears them.

## 9. Reference-sweep strategy (AC-002, AC-005, AC-011)

The migration is only "done" when no *live* reference to an old path or old command
name remains. The sweep is a **documented, re-runnable verification procedure** the
Coder runs and the Reviewer re-runs — not a new CI gate (adding a gate is a
governance change, out of scope; automating this is a BACKLOG candidate). It runs
over **tracked files only** (`git grep`, which respects the index).

### 9.1 Old artifact paths (AC-002)

Run, from the repo root:

```
git grep -nE '(^|[^a-zA-Z0-9_/-])(specs/|docs/adr|docs/traceability|retros/)'
```

Every hit must be either (a) rewritten to its `project/…` form, or (b) on the
**allowlist** of legitimate historical/quotation text:

- `project/specs/project-workspace/spec.md` — the "Sources" reference-inventory
  line ("17 references to `specs/`, 11 to `docs/adr/`…") and the AC-002 text that
  *names the old paths as search targets*. These describe the migration; they are
  not pointers to those locations.
- `project/specs/project-workspace/design.md` (this file) — the migration-map "From"
  column and prose that necessarily quote old paths.
- `aidsef-framework-development-content/adr/002-*.md` and the moved build-order /
  playbook where they narrate history ("`docs/adr/` → `project/adr/`").

The allowlist is **enumerated in the PR description** so the check is auditable, not
a silent escape hatch. Any hit not rewritten and not on the allowlist fails the
sweep.

### 9.2 Old command names (AC-011)

```
git grep -nE 'aidsef-(spec|design|plan|build|retro)\b'
```

The numbered names (`aidsef-1-spec`, …) do **not** match this pattern — the digit
breaks the old substring — so a clean rename yields only: (a) hits to rewrite to the
new command, and (b) allowlisted quotations (the AC-011 text listing the old names
as search targets; this design's ADR-003 discussion). Same enumerate-in-PR rule.

### 9.3 Out-of-scope boundary — `resident-build.yml`

The spec lists the `resident-*` workflows as out of scope, yet AC-011 says *no*
tracked file may keep an old command reference, and `resident-build.yml` invokes
`/aidsef-build` (lines 56–57). Resolution: the sweep makes the **minimal mechanical
string edit** `/aidsef-build` → `/aidsef-4-build`. This changes no logic and does
not enable the shipped-disabled workflow, so it honors both AC-011 and the
out-of-scope intent (no functional change to resident workflows). Flagged here so
the boundary call is explicit, not silent.

### 9.4 Link-integrity for the playbook move (design consideration, flagged)

The playbook moves into `aidsef-framework-development-content/` (§3.3), which clones
**delete** at trim. Two *keep-forever* clone documents hard-link into the playbook:
`constitution.md` (Phase-0 lifecycle link; SEV-callout link) and
`.claude/agents/README.md` (playbook §2 link). Rewriting these to
`aidsef-framework-development-content/playbook/…` would dangle in a trimmed clone.

Proposed handling: convert those specific deep-links to **absolute URLs at the
public upstream template repo** (`https://github.com/rossiter78/aidsef/blob/main/aidsef-framework-development-content/playbook/…`),
which resolve regardless of trim, with an unlinked-plain-text fallback ("see the
AIDSEF playbook") if linking upstream is undesired. `README.md` and `CLAUDE.md`
are template documents a clone **replaces** (build-order Phase D step 5), so their
playbook links may point at the framework folder directly. **This upstream-URL
choice is the one notable open call in this design — see §12.** Note: AC-002 does
*not* sweep for `docs/playbook/` (it lists only the four artifact roots), so this is
a self-consistency concern the design raises, not a criterion mandate.

## 10. Error handling & edge cases

- **Case-insensitive filesystem (Windows dev host).** Every move changes the path
  substantively (new parent folder), so no pure directory-case rename is required;
  `git mv` is safe. CI runs on Linux.
- **Rename detection defeated by big diffs.** Mitigated by ADR-002's move-then-edit
  commit discipline.
- **Empty-directory tracking.** Git does not track empty folders; each `project/`
  subfolder is kept non-empty by its `README.md` (AC-001), so the structure survives
  a fresh clone. `project/inputs/` likewise ships with its README.
- **Trim ordering independence (AC-016).** Because framework ADRs live in the
  framework folder and `project/adr/` ships README-only, a clone that inspects
  before trimming, or trims in either order, never sees a stray `project/adr/001`.
- **Migration-PR traceability gate.** See §11.1 — most ACs here are
  structural/documentation and are not `Covers:`-annotatable; this is expected for
  an infrastructure change and is called out for the Planner.

## 11. Acceptance-criteria → component map

| AC | Satisfied by | Verified by |
|---|---|---|
| **AC-001** | §3.1/§3.2 — five `project/*` READMEs (specs, adr, traceability, retros moved+reworded; inputs new), each stating who-writes / which-phase | inspection |
| **AC-002** | §3 migration + §9.1 sweep — every old artifact-path reference rewritten to `project/…` | §9.1 `git grep` + allowlist |
| **AC-003** | §4.1 tool `SPEC_GLOB`/`OUT_DIR`; §4.2 test fixtures moved to `project/specs`/`project/traceability` | test suite (a test `Covers: AC-003`) |
| **AC-004** | §4.3 `ci.yml` upload path; §5.1 `claude-review.yml` prompt → `project/specs/`, `project/adr/` | inspection / CI run |
| **AC-005** | §5.4 charter sweep + §5.3 skill paths — every artifact path in charters/skills is `project/…` | §9.1 sweep scoped to `.claude/` |
| **AC-006** | §6 `project/inputs/README.md` content | inspection |
| **AC-007** | §5.3 `aidsef-1-spec` reads `project/inputs/` + spec Sources section | inspection |
| **AC-008** | §5.3 `aidsef-2-design` reads `project/inputs/` + design Sources section | inspection (this design's §11) |
| **AC-009** | §6 "merged spec wins" in `inputs/README.md` + `analyst.md` + `architect.md` | §9 sweep for the sentence in 3 files |
| **AC-010** | §5.2 five skills renamed `aidsef-<n>-<phase>`; ADR-003 | slash-menu inspection |
| **AC-011** | §5.2 old dirs removed (no alias) + §9.2 sweep | §9.2 `git grep` + allowlist |
| **AC-012** | §7 guide states Phase 5 has no command (auto on PR) | inspection |
| **AC-013** | §7 phase→command→output table | inspection |
| **AC-014** | §7 working-with-inputs section | inspection |
| **AC-015** | §7 two-step trim; §3 folder partition makes it complete | inspection |
| **AC-016** | §3.3 ADR-001–004 → framework folder; `project/adr/` README-only; ADR-004 | inspection (`ls project/adr/`) |
| **AC-017** | §3.4 root `BACKLOG.md` replaced empty; §3.3 content → framework folder | inspection |

### 11.1 Note for the Planner — traceability on the migration PR

Only AC-003 (and the tool-path half of AC-004) is unit-testable with a `Covers:`
annotation; the other fifteen ACs assert file existence, README wording, and doc
content, which `check_traceability.py` cannot test. This is inherent to a
structural/docs change, not a gap. The mechanical proofs are the **§9 reference
sweeps** (for AC-002/005/009/011) and **inspection** (the rest). The Planner should
therefore expect the migration PR to carry pending (UNCOVERED) criteria for the
structural ACs and rely on the existing `--allow-uncovered` semantics plus the
High-tier human gate — **not** a change to `ci.yml`'s mode logic (governance is out
of scope). Recommend sequencing the tool/test edits and the doc/structure moves so
the reviewer can read moves, then machinery, then docs.

## 12. Open calls & uncertainties (for the design-approval gate)

1. **Playbook deep-links in keep-forever clone docs (§9.4).** The playbook moves
   into the trim-deleted framework folder, but `constitution.md` and
   `.claude/agents/README.md` link into it. Proposed: absolute upstream-repo URLs
   (fallback: unlinked plain text). This introduces a coupling to the public
   upstream repo that the spec did not explicitly bless — **please confirm the
   upstream-URL approach or choose the plain-text fallback at the gate.** Not a
   criterion (AC-002 does not sweep `docs/playbook/`), so no criterion is weakened
   either way.
2. **Splitting one feature's artifacts across two trees (§8, ADR-004).** The
   project-workspace spec/design live under `project/specs/` while its ADRs live in
   the framework folder. Defensible (framework-dev ADRs must not travel to clones),
   but it is an asymmetry worth a human nod.

Neither is a blocker; both are recorded rather than guessed. No `needs-human` issue
is filed because the design is buildable as written and these are gate-time
confirmations, not blocks.

## Sources

Per the provenance convention this feature introduces (AC-008):

- The approved [`spec.md`](spec.md) (PR #20) — the 17 acceptance criteria and the
  target-layout table are its source of truth.
- `constitution.md` — core rules 3 (ADRs) and 6 (audit trail), §3.2 (risk tiers),
  §4 (test append-only), §8 (amendments).
- Direct inspection of the current codebase: `tools/check_traceability.py`,
  `.github/workflows/{ci,claude-review,resident-build}.yml`,
  `.github/ISSUE_TEMPLATE/task.yml`, the nine `.claude/agents/*.md` charters, the
  five `.claude/skills/aidsef-*` skills, `docs/00-getting-started.md`, `README.md`,
  `CLAUDE.md`, `docs/adr/001` + its README, and the existing folder READMEs.
- Reference sweep of the repo (§9) establishing the migration surface: old
  artifact-path references across 24 tracked files; old command-name references
  across the charters, skills, workflows, and issue template.
- No `project/inputs/` documents existed for this feature (the feature *creates*
  that folder); the requirements came from the spec and codebase above.
