# AIDSEF — Commercialization & the skeptic's brief

> Section 6 of the AIDSEF playbook. Decided 2026-07-18.
> Positioning: **you are not selling AI; you are selling governance for AI.**
> Engineers keep exactly the authority they have today; what changes is who does the labor — and every quality claim is mechanically checkable.

## 1. Product form: open-core

[Open-core](../glossary.md#open-core) means the framework itself is free and public, while services and premium extras are paid.

**Open (public GitHub, permissive license):**
- The playbook (these six sections) and the methodology.
- The template repository: constitution template, role charters, skills, hooks, CI workflows, LiteLLM config.
- The `red-proof` CI job — published as a standalone GitHub Action. "Provable TDD" stands on its own as a lead magnet, independent of the rest of AIDSEF.

**Paid:**
- Pilot engagements (workshop + build + readout).
- Support/updates subscription for adopting teams.
- Premium modules: the sovereign profile (fully-local Hermes orchestration for privacy-sensitive clients), metrics/readout dashboards, notification bridges, second-reviewer integrations.
- Constitution workshops and team enablement.

Accepted trade-off: competitors can run the open playbook. Mitigation: the moat is the engagement track record, the metrics library, and the premium modules — plus the AIDSEF name/trademark stays yours.

## 2. First market: SMBs needing internal tools

Small and mid-sized businesses that need internal tools: fastest sales cycle, no engineering organization to offend, low-risk projects. Every delivery grows the metrics library. Skeptic-heavy organizations (agencies, software teams) are the second wave, approached with those case studies plus the open-source credibility engine.

### 2.1 Primary user persona (core positioning)

The AIDSEF user is typically **not a professional software engineer**: an operations lead, analyst, founder, or domain expert who wants to build software with AI *responsibly* — and who must face the skeptical engineers in or around their organization. AIDSEF gives them three things at once:

1. **A way to build** that produces professionally-governed software, not unreviewable AI output.
2. **An education** — using the framework teaches proper software engineering practice as a side effect (specs, tests, reviews, decision records), in plain language. The [glossary](../glossary.md) is part of the product.
3. **A peace treaty with the engineers** — every gate, check, and audit trail exists so the professional engineers can *verify* rather than *trust*.

Internal framing (never public-facing): this is *legitimized vibe coding*. The deliberately professional name — AI-Driven Software Engineering Framework — is itself part of the positioning: it signals to engineers that this is their discipline, applied, not bypassed.

Documentation consequence: all repo content is written for the non-engineer first, with engineering terms defined on first use; the skeptical engineer is the secondary reader, served by the **Software Engineering Validation** callouts throughout these docs.

## 3. The skeptic's brief

When an engineer asks "why should I trust software built this way?", the answer is not "trust the AI" — it's "here is the established engineering practice each piece implements, and here is how you can check it yourself." That mapping is the skeptic's brief:

> **Software Engineering Validation:**
>
> | AIDSEF element | Established practice it implements | Verify by |
> |---|---|---|
> | Given/When/Then specs | User stories + acceptance criteria (BDD) | Reading the spec PR you approved |
> | ADRs with alternatives | Architecture Decision Records | Interrogating any decision's recorded trade-offs |
> | Red proof | TDD (Beck), made auditable | Re-running the CI job proving tests failed first |
> | Branch protection + human gates | Code review + change control, unchanged | Your own GitHub org settings |
> | Traceability matrix | Requirements traceability (regulated norm) | CI fails on any uncovered criterion |
> | Risk-tiered gates | Change-management risk classes | Re-tiering anything with one label |
> | Retro loop | Agile retrospectives, data-driven | Every process change arrives as a PR you approve |

Closing argument: the red proof, live traceability, and reviewing 100% of pull requests are practices human teams *claim* but rarely sustain — because they're tedious. AIDSEF sustains them because agents don't get bored. **The framework is more disciplined than most human teams — provably.**

**Independent validation:** Google's May 2026 whitepaper [*The New SDLC with Vibe Coding*](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding) (Osmani, Saboo & Kartakis) draws the same line AIDSEF is built on: the difference between casual vibe coding and what it calls [agentic engineering](../glossary.md#agentic-engineering) is not which AI you use, but how much structure, verification, and human judgment surrounds the AI's output. Its verdict — "structure scales, vibes don't" — and its finding that most agent failures trace back to the surrounding scaffolding rather than the model are AIDSEF's pitch, stated in an independent, Google-published source. Where the paper prescribes principles (specs first, tests as the contract with the AI, a versioned and human-owned harness, risk-appropriate model routing), AIDSEF ships the machinery that enforces them.

### Objection handling

- *"AI code is slop"* → the red proof, cross-model review, structured findings, and human gates on everything high-risk.
- *"Our code can't leave the building"* → local models (Apache 2.0-licensed) on the client's own hardware; the sovereign profile.
- *"Vendor lock-in"* → roles are aliases; LiteLLM repoints any role to another vendor in one line; the Coder is an [open-weight](../glossary.md#open-weight-model) model.
- *"You're replacing our engineers"* → engineers move *up*: authors of the constitution, approvers of every gate. Authority unchanged; toil removed.
- *"Compliance?"* → the audit trail is the repository history itself; traceability is generated on every pull request.

## 4. Proof metrics (auto-collected)

Lead with [DORA metrics](../glossary.md#dora-metrics) — the software industry's shared yardstick for delivery performance: how often you ship, how long a change takes to reach users, how often a change breaks something, and how fast you recover when it does.

> **Software Engineering Validation:** DORA four (deployment frequency, lead time for changes, change-failure rate, time-to-restore) as the headline. Supporting: escaped defects, findings per KLOC, coverage + mutation scores, escalation rate, human-minutes per merged feature, and cost per merged task (LiteLLM telemetry + amortized subscription). Readouts are client-baseline vs. AIDSEF.

## 5. Pilot engagement model

1. **Week 1 — Constitution workshop.** The client's senior engineers co-author the constitution (gates, tiers, coverage, model policy). Co-authorship converts the loudest skeptic into a co-designer.
2. **Weeks 2–5 — Pilot build** of a bounded internal tool, at autonomy Level 0–1, with the client's engineers holding every gate.
3. **Readout.** Metrics vs. their baseline, plus the full audit trail. Decision: license/expand — or they keep a working tool regardless (a no-lose offer).
