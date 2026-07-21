# 006. Slim the constitution's adoption block; give the autonomy level one home

- Status: accepted
- Date: 2026-07-21
- Feature: framework onboarding (precursor to the `/aidsef-begin` skill)

## Context

The top of `constitution.md` carried a five-row "Ratification" table that a new project filled in when cloning: Project, Ratified by, Date, Operating profile, Autonomy level. Reviewing it against what the machinery actually reads turned up two problems:

1. **Three rows are busywork.** Project, Ratified by, and Date are read by no hook, workflow, or tool. They also duplicate what Git already records for free: core rule 6 says "the audit trail is the repository history itself," and the merge commit of the constitution's own pull request already captures **who** approved it, **when**, and in **which** repository. The table asked a human to re-type, by hand, what Git records automatically.

2. **The autonomy row was a second, competing copy.** The table stated the autonomy level (e.g. "0 — Watched"), but the value the automation actually acts on is a **separate GitHub repository variable**, `AIDSEF_AUTONOMY_LEVEL`, read by the resident-runner workflow (`.github/workflows/resident-build.yml`: `if: vars.AIDSEF_AUTONOMY_LEVEL == '2'`). Two places holding the same setting can drift — the table could say "0" while the variable said "2", and the machinery would follow the variable. Compounding this, §6 claimed the level "moves only by amendment," which does not match a setting that a human flips in GitHub's settings UI.

The *act* of ratification — a human approving the constitution's first PR — is not busywork: it is the governance keystone (a person formally adopts the rulebook before any agent runs) and it costs nothing extra, because it is the same PR approval every file gets.

## Decision

**Keep the adoption act; remove the busywork; give the autonomy level exactly one home.**

- **Drop** the Project, Ratified by, and Date rows. Git records that provenance.
- **Rename** the section from "Ratification" to **"Project settings"**, and state the two real settings as prose: **Operating profile** (Solo default; a team profile is an amendment, §8) and **Autonomy level**.
- **Autonomy lives only in the `AIDSEF_AUTONOMY_LEVEL` GitHub variable.** The constitution documents the default (0 — Watched) and points at the variable as the single switch, rather than holding a competing value. §6 is reworded: the level lives in the GitHub variable the resident-runner reads, and **only a human changes it, only when the trust milestones are met** — replacing the inaccurate "moves only by amendment."
- **Keep the adoption prose:** approving the constitution's PR is Phase 0. A short note in the settings section says Git records who adopted it and when, so there is no form to fill in.

## Alternatives considered

- **Leave the block as-is.** Rejected: it is hand-entered duplication of Git plus a drift-prone second copy of the autonomy switch — the exact kind of "two sources that can disagree" the framework warns against elsewhere.
- **Remove the whole section.** Rejected: a one-glance summary of "how is this project configured" (profile + where autonomy lives) is useful at the top of the rulebook; only the busywork and the competing copy needed to go.
- **Make the constitution the source of truth for autonomy and have CI read it.** Rejected as scope creep: the enforcing workflow already reads a GitHub variable, that is a reasonable home for an operational switch, and rebuilding that plumbing is a bigger change than this cleanup warrants.

## Consequences

- **Easier:** less onboarding data-entry (which directly simplifies the forthcoming `/aidsef-begin` wizard — fewer things to prompt for); one autonomy switch instead of two that can disagree; provenance still fully recorded, by Git.
- **Watch for / flagged for the human reviewer:** §6 no longer calls raising the autonomy level a constitution "amendment." Raising it stays **human-only and milestone-gated**, but the mechanism is now honestly described as changing the GitHub variable, not editing this file. This is a deliberate wording change to a governance rule and is called out here so the approval is eyes-open.
