# Inputs

**You (the human) write here — before the lifecycle starts.** This is the intake folder for material you already have when you begin work: prior specs, plans, designs, research notes, whitepapers — anything that should inform what gets built. It is read during the earliest phases (spec and design); nothing lands here from a later phase.

## What goes here

Pre-existing documents: prior **specs, plans, designs, and research**. Drop them in as-is — there is no required format or naming. The agents read whatever you place here.

## What the agents do with it

- The **Analyst** reads `project/inputs/` before interviewing you, during **Phase 1 (spec)** — treating what it finds as background, not gospel.
- The **Architect** reads `project/inputs/` during **Phase 2 (design)**.
- Both cite what they actually drew on: the produced `spec.md` and `design.md` each carry a **Sources** section listing every input document they used (or stating that none existed).

## The governing rule

Once a spec covering the material merges, **the merged spec governs**. The input document stays exactly as you left it — an unmodified historical record of where the requirements came from. If a merged spec and an input document ever disagree, there is one rule:

> **The merged spec wins; inputs are historical once absorbed.**

## What never happens

No agent ever modifies or stamps an input document. Absorption is recorded in the spec (through its Sources section), never written onto the input itself. Your originals are left untouched.
