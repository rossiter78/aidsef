# 002. Preserve file history with `git mv` during the workspace migration

- Status: proposed
- Date: 2026-07-20
- Feature: project-workspace

## Context

The `project-workspace` feature relocates almost every artifact directory in the
repository: `specs/` → `project/specs/`, `docs/adr/` → (framework ADRs)
`aidsef-framework-development-content/adr/`, `docs/traceability/` →
`project/traceability/`, `retros/` → `project/retros/`, the playbook and
build-order doc into `aidsef-framework-development-content/`, and `BACKLOG.md`
content into the framework folder. This is a bulk move of existing tracked files
to new paths, not the creation of new content.

The constitution makes the repository history load-bearing: core rule 6 — "If it
isn't in Git, it didn't happen. … The audit trail is the repository history
itself." Every spec, ADR, review, and retro is meant to be answerable later with
`git log`/`git blame`. How we perform the move decides whether that lineage
survives the restructure.

Two mechanically different ways to land the same end-state:

1. **Rename in place (`git mv`)** — Git records each file as a rename; `git log
   --follow` and `git blame` trace straight through the move into the file's full
   prior history.
2. **Delete + recreate** — remove the file at the old path and add fresh content
   at the new path in the same commit. The end tree is identical, but Git sees an
   unrelated delete and add: blame resets at the migration commit and the prior
   history is severed unless a reader manually digs before the move.

## Decision

**Perform the migration with `git mv` (pure renames) wherever a file's content is
substantially carried over, and keep content edits in separate follow-up commits
from the moves.**

Concretely, the build does, per relocated file: `git mv <old> <new>` first, commit
the moves, then apply the reference-sweep edits (path fixes, README wording) in
subsequent commits. Renames and edits are not squashed together, so Git's
rename-detection is not defeated by a large simultaneous content diff on the same
file.

Files that are genuinely replaced rather than moved (the root `BACKLOG.md`, which
ships empty per AC-017; the new clone-facing guide at `docs/00-getting-started.md`)
are add/replace operations, not renames — their "history" is the new file, which
is correct because their content is new.

## Alternatives considered

- **Delete + recreate for everything.** Simpler to script (write the new tree,
  delete the old), and the working tree is byte-identical to the `git mv` result.
  Lost on the audit trail: it discards `git blame`/`--follow` lineage for every
  spec, ADR, and retro in the repo — exactly the records the constitution says the
  history exists to preserve. A future reader asking "why is this acceptance
  criterion worded this way?" would hit a wall at the migration commit. The
  end-state parity is not worth severing the provenance the framework sells.
- **One giant commit mixing moves and content edits.** Rejected: a rename with a
  large content change on the same file can fall below Git's rename-detection
  similarity threshold, silently degrading the move into a delete+add and losing
  the very history `git mv` was chosen to keep. Separating moves from edits keeps
  rename detection reliable and makes the migration PR reviewable (the human sees
  "these are pure moves" then "these are the edits").

## Consequences

- **Easier:** `git blame`/`git log --follow` keep working across the restructure;
  the migration PR is reviewable in two legible passes (moves, then edits); the
  audit-trail guarantee the framework markets survives its own biggest reshuffle.
- **Harder / watch for:** the build must be disciplined about commit ordering
  (move, then edit) rather than letting an agent regenerate files at new paths from
  scratch. On case-insensitive filesystems (this repo is developed on Windows) a
  pure directory-case change would need care, but every move here changes the path
  substantively, so that edge case does not arise.
