# 003. Numbered skill command names, and clean removal of the old names

- Status: proposed
- Date: 2026-07-20
- Feature: project-workspace

## Context

AIDSEF drives each lifecycle phase from a Claude Code **skill** — a directory
under `.claude/skills/` whose name becomes the slash-command a human types.
Today they are `aidsef-spec`, `aidsef-design`, `aidsef-plan`, `aidsef-build`,
`aidsef-retro`. In Claude Code, **a project skill's command name is its directory
name**; there is no separate command-name field and no first-class alias
mechanism, and colons are reserved for plugin namespaces (see the build-order
doc, Phase A step 4). So the command string and the directory name are the same
lever — you cannot rename the command without renaming the directory, and you
cannot ship two names for one skill without shipping two directories.

The spec fixes the target names (AC-010): `aidsef-1-spec`, `aidsef-2-design`,
`aidsef-3-plan`, `aidsef-4-build`, `aidsef-6-retro`. The number encodes the phase
so the slash-command menu reads in lifecycle order. Phase 5 (review) has no
command because it runs automatically on every pull request — hence the gap
between `4-build` and `6-retro` (AC-012).

Two things are still open and interact:

1. **The number's placement.** `aidsef-1-spec` (infix) versus `1-aidsef-spec`
   (prefix) versus `aidsef-phase1-spec`.
2. **What happens to the old names.** AC-011 requires that after the rename, **no
   reference to the old command names remains as a command reference in any tracked
   file.** But muscle memory and any external notes point at the old names, so
   there is a real question of whether to leave a redirect/alias behind.

## Decision

**Rename each skill directory to the numbered infix form (`aidsef-<n>-<phase>`)
and remove the old directories outright — ship no alias, shim, or redirect skill.**

- Infix (`aidsef-N-phase`) keeps the shared `aidsef-` prefix first, so all five
  commands still cluster together alphabetically in the menu *and* sort into phase
  order within the cluster. A leading number (`1-aidsef-spec`) would scatter them
  to the top of the menu and break the brand-prefix grouping; `aidsef-phase1-spec`
  is longer to type for no extra clarity.
- The old-named directories are deleted in the same move (`git mv
  .claude/skills/aidsef-spec .claude/skills/aidsef-1-spec`, etc. — a rename, per
  ADR-002), leaving nothing behind that AC-011's sweep could match as a live
  command reference.
- Every remaining mention of an old command name in a tracked file is either
  rewritten to the new name (live references: charters, other skills, README,
  issue templates, the disabled `resident-build.yml`) or is a quotation of the old
  name as a search target inside this feature's own spec/design/ADR text, which is
  historical description, not a command reference (see the design's reference-sweep
  allowlist).

## Alternatives considered

- **Keep old directories as deprecated alias skills that print "renamed to
  `aidsef-1-spec`, use that instead."** Rejected on two counts. First, it directly
  violates AC-011: a redirect skill *is* a tracked file naming the old command, so
  the sweep can never reach zero. Second, Claude Code has no alias primitive — an
  "alias" is a full second skill that clutters the command menu with dead entries,
  the exact menu-legibility problem the numbering is meant to fix. The muscle-memory
  cost is a one-time re-learning for a solo operator, cheap next to permanent menu
  clutter and a criterion that can never pass.
- **Leave the names unchanged (`aidsef-spec` …).** Rejected: it fails AC-010's
  requirement that the menu show phase order, which is the feature's point — a
  fresh clone's operator cannot currently predict the sequence from the menu.
- **Number prefix (`1-aidsef-spec`) or verbose (`aidsef-phase1-spec`).** Rejected:
  prefix breaks the `aidsef-` grouping and pulls the commands away from the rest of
  the project's namespace; verbose adds typing without adding information the single
  digit already conveys.

## Consequences

- **Easier:** the slash-command menu reads as a numbered lifecycle; a new clone's
  operator learns the phase order for free; there is exactly one name per phase, so
  no stale command can be invoked by accident.
- **Harder / watch for:** anyone with the old names in muscle memory or in external
  notes must relearn; because there is no redirect, an old-name invocation simply
  finds no command (a clean "unknown command", not a silent wrong action). The
  build must update the command string inside the disabled `resident-build.yml`
  too — a mechanical name fix with no behavioral change to a shipped-disabled
  workflow — so AC-011's "any tracked file" holds without reopening the
  out-of-scope resident workflows.
