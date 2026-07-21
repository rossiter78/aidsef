# 007. `/aidsef-begin` — a one-time onboarding wizard, not a bootstrap script

- Status: accepted
- Date: 2026-07-21
- Feature: framework onboarding

## Context

Setting up a new project from the AIDSEF template is a fixed sequence — getting-started Phase D steps 4–9: trim the framework-authoring files, write the project's own `README.md`/`CLAUDE.md`, complete two browser-only GitHub settings, run `setup-repo.sh`, and adopt the constitution. Until now those steps existed only as chat guidance, and running dogfood project #1 by hand showed how easy it is to miss one or do them out of order (the two browser settings, in particular, must be done *before* the first pull request or the AI review can't run on it).

Two shapes could automate this: a **bootstrap script** or a **Claude Code skill**. And a handful of design points needed settling: what exactly to remove for a clean clone, how many pull requests setup produces, and whether the wizard has its own role.

## Decision

**Ship `/aidsef-begin` as a one-time onboarding skill (charter-less orchestrator).** A skill can *interview* the human — ask what the project is, its hard rules, whether they have planning documents — and draft the project's `README.md`/`CLAUDE.md` from the answers; a script cannot. It runs once, right after the human clones their new project.

Settled design points:

- **Cleanup for a truly fresh clone.** The wizard deletes the framework-authoring material: `docs/playbook/`, `docs/00-getting-started.md`, **every framework `docs/adr/NNN-*.md`** (keeping `docs/adr/README.md`, so the clone starts its own ADR numbering at `001`), and empties `BACKLOG.md`. This resolves the item left open in [ADR-005](005-project-workspace.md) — a clone no longer inherits the framework's own decision records. Everything a project runs on is kept: `constitution.md`, all of `.claude/`, `.github/`, `docs/glossary.md`, `scripts/`, `tools/`, `tests/`, and the `specs/` / `retros/` / `docs/traceability/` / `project/inputs/` folders (each ships as just a README).

- **One setup pull request, not two.** The trim, the new `README.md`/`CLAUDE.md`, any `project/inputs/` documents, and any constitution tuning all land in a single `Set up <project>` PR. Approving it **is** Phase 0 — adopting the constitution. For a solo operator this is one approval instead of two; the governance meaning is intact because the rulebook is part of what is being approved. (Following [ADR-006](006-slim-adoption-block.md), there is no separate ratification form to fill in — Git records who adopted it and when.)

- **The wizard has no charter.** Like `/aidsef-4-build` coordinating the Test Engineer and Coder, `/aidsef-begin` is an orchestrator; it talks to the human directly and needs no new role among the nine.

- **The wizard is kept, not self-deleted.** It stays in `.claude/skills/` after running, so a human who wants to start setup over can re-run it. The one-time nature is documented, not enforced by removal.

- **The browser steps are a hard hand-off.** Adding the `CLAUDE_CODE_OAUTH_TOKEN` secret and granting the GitHub App access are actions only the human can take (and that an agent must never attempt). The skill pauses, gives links, and waits for confirmation — and does so *before* opening the PR, so review works on the first PR.

The template's `README.md` carries the pre-wizard steps (Use this template → `git clone` → open in Claude Code → run `/aidsef-begin`), because those happen before the skill can exist locally.

## Alternatives considered

- **A post-clone bootstrap script.** Rejected: a script can trim files and run `setup-repo.sh`, but it cannot interview the human or draft a project-specific `README.md`/`CLAUDE.md`. The interview is the point — it is what turns a generic template into *this* project.
- **Two pull requests (a chore/bootstrap PR, then a separate constitution-adoption PR).** Rejected for the solo default: it doubles the approvals for no added safety. A team profile that wants the constitution adopted as its own ceremonial PR can still split it — this is a default, not a rule.
- **Self-deleting wizard.** Rejected on the human's call: keeping it costs one dormant menu entry and buys the ability to re-run setup from scratch, which is worth more than a tidy menu.

## Consequences

- **Easier:** new-project setup is a single guided command ending in one approval; the delicate "browser settings before the first PR" ordering is enforced by the wizard's pause instead of living in a human's memory; clones no longer inherit framework ADRs.
- **Watch for:** the wizard is instruction-only at the browser step — it must never try to add secrets or grant app access. On Free-plan private repos, `setup-repo.sh`'s branch-protection calls warn rather than succeed; the wizard should report that as the known trade-off, not an error. Because setup lands as one PR under branch protection, the two browser steps genuinely have to be finished first, or the PR's review check cannot run.
