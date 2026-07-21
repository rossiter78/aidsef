# 005. Project workspace: an inputs folder and numbered lifecycle commands — scoped as an ADR, not a feature

- Status: accepted
- Date: 2026-07-21
- Feature: project-workspace (framework process change)
- Supersedes: ADR-002 and ADR-004 (mechanics of a larger repository migration that was reverted) and ADR-003 (the numbered-command-name decision, which is retained and folded in below); also folds in the decision written up as `specs/project-workspace/{spec,design}.md` before this reset

## Context

Someone cloning the AIDSEF template to start their own project hit two small friction points:

1. **No home for documents they already had.** Prior plans, research, and draft specs got parked wherever seemed reasonable (dogfood project #1 improvised a `docs/assessment/` folder), and the lifecycle agents didn't know to look there.
2. **The slash-command menu didn't show phase order.** The commands were `aidsef-spec`, `aidsef-design`, `aidsef-plan`, `aidsef-build`, `aidsef-retro` — a newcomer couldn't read the sequence, or tell that review (Phase 5) has no command because it runs automatically on every pull request.

Both are real, both are small: a folder plus a wording-and-naming change. There is **no product code** and no behavior that can silently break.

The trap we fell into first: this was written up as a `spec.md` with **17 numbered acceptance criteria**, a `design.md`, three ADRs, and a folder migration that relocated every artifact directory under a new `project/` tree. Because `tools/check_traceability.py` globs `specs/*/spec.md`, the moment the change existed as a findable spec the full TDD / red-proof / traceability apparatus clamped onto what is really a folder-and-wording change — and satisfying it invited a grep-test per prose criterion, which checks token presence, not whether a doc is accurate or clear. See the retrospective note below.

## Decision

**Treat framework process / folder-structure / documentation changes as ADR-level decisions, not spec-with-testable-acceptance-criteria features.** Record the decision and what shipped in an ADR, make the edits, and verify with **one human doc-consistency review** — not the spec → AC → TDD → traceability lifecycle, which exists for product code.

Under that scope, this change ships exactly two goals:

1. **`project/inputs/` — an intake folder the lifecycle reads by default.** The human drops pre-existing material there. The Analyst reads it before interviewing (Phase 1) and the Architect reads it during design (Phase 2); the produced `spec.md` and `design.md` each carry a **Sources** section listing what they drew on. The governing rule, stated in `project/inputs/README.md` and in the Analyst and Architect charters: **the merged spec wins; inputs are historical once absorbed** — no agent ever modifies an input document.

2. **Numbered lifecycle commands.** The five skills are renamed `aidsef-1-spec`, `aidsef-2-design`, `aidsef-3-plan`, `aidsef-4-build`, `aidsef-6-retro`, so the menu reads in phase order. The gap at 5 is deliberate — review runs automatically on every PR, so it has no command. The number is an **infix** (`aidsef-<n>-<phase>`, not `<n>-aidsef-…`) so all five keep their shared `aidsef-` prefix and cluster together in the menu while sorting into phase order within the cluster. The old directories are removed outright with **no alias or redirect**: in Claude Code a skill's command name *is* its directory name and there is no alias primitive, so an "alias" would only be a second, dead menu entry — an old-name invocation cleanly finds no command rather than silently doing the wrong thing.

Everything else the discarded spec proposed — moving all artifact directories under `project/`, a deletable `aidsef-framework-development-content/` folder, shipping `project/adr/` README-only, an empty root `BACKLOG.md` — is **dropped**. Those changes served a tidiness goal neither of the two real goals needs, and cost ~25 path edits across charters, skills, workflows, and the traceability tool. The folder moves were reverted with `git mv` (history preserved); the artifact directories stay at their root paths (`specs/`, `docs/adr/`, `docs/traceability/`, `retros/`), where the machinery already reads them.

> **Software Engineering Validation:** This ADR *is* the lightweight change-control record for a structural refactor: an intake convention plus a command-namespace rename. It carries no traceability matrix because there is no runtime behavior to trace — the acceptance check is human review of documentation consistency (a `git grep` sweep proving no stale path or command reference survives), not an executable test suite. Full spec→AC→TDD rigor is reserved for `src/**` changes whose regressions are silent.

## Alternatives considered

- **Run it through the full spec/AC/traceability lifecycle (what we did first).** Rejected in hindsight: it over-engineered a folder-and-wording change into a 17-AC feature, produced a traceability paradox, and wasted a working session. The framework must not crush simple process/docs changes with its own code-oriented machinery — real users cloning AIDSEF will need to tweak the framework itself and cannot be forced through a feature lifecycle to move a folder.
- **Keep the migration — leave everything under `project/` and sweep the ~25 references to it.** Rejected: more work than the revert for structure that neither goal needs, and it leaves `main` inconsistent until every charter/skill/workflow/tool is re-pointed. Reverting re-consistifies `main` for free because those files already name the root paths.

## Consequences

- **Easier:** `main` is internally consistent again; the two goals land as a small, reviewable PR; a newcomer reads the phase order from the menu and knows where to put existing documents. `git blame`/`--follow` survive the revert because it used pure renames.
- **A recorded lesson (retrospective):** scope changes proportionately. A future **"Executive" change class** is planned — a decision implemented outside the full process, where the human explicitly owns the risk — for exactly this kind of framework/config edit. Until then, the rule of thumb: if the change is prose, directory layout, or configuration with no silently-breakable behavior, it is an ADR, not a spec.
- **Deliberately out of scope (unchanged pre-existing state):** a clone still inherits the framework's own `docs/adr/001`–`004`; consolidating framework-only material away from clones was the discarded migration's goal, not one of the two we kept. If it proves worth doing later, it returns as its own small, ADR-scoped change.
