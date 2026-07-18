# AIDSEF — AI-Driven Software Engineering Framework

A framework for building software with AI agents **responsibly**: the AI does the labor, humans keep the authority, and every quality claim can be checked by machinery rather than taken on trust. You describe what you want in plain conversation; specialist AI agents write the specifications, tests, code, and reviews — and nothing ships without passing the checkpoints you control.

You don't need to be a software engineer to use AIDSEF. You will, as a side effect, learn how disciplined software engineering actually works — every technical term in these docs is defined in plain language in the [glossary](docs/glossary.md), and each doc carries **Software Engineering Validation** callouts where professional engineers can verify the rigor in their own vocabulary.

**Status:** design complete (2026-07-18); template repo build-out in progress.

## The playbook

1. [Process flow & governance](docs/playbook/01-process-and-governance.md) — the lifecycle, risk-based human checkpoints, solo/team profiles, and the self-improvement loop
2. [Roles & model matrix](docs/playbook/02-roles-and-model-matrix.md) — 9 AI agent roles; top-tier cloud models for judgment, local models on your own hardware for volume; human-approved escalation
3. [Toolchain & interfaces](docs/playbook/03-toolchain-and-interfaces.md) — how Claude Code, GitHub, LiteLLM, and vLLM connect; subscription-only Claude billing; autonomy levels 0–2
4. [Quality system](docs/playbook/04-quality-system.md) — the red proof, role-separation guardrails, requirement-to-test traceability, coverage gates, the review→triage loop
5. [Human experience](docs/playbook/05-human-experience.md) — the zero-terminal guarantee; VS Code, Claude Desktop, and GitHub are the only surfaces a human ever touches
6. [Commercialization](docs/playbook/06-commercialization.md) — open-core model, the skeptic's brief, DORA-based proof metrics, pilot engagement shape

Plus: [Getting started (build order)](docs/00-getting-started.md) · [Glossary](docs/glossary.md) · [Backlog](BACKLOG.md)

## Core decisions at a glance

| Dimension | Decision |
|---|---|
| Backbone | Claude Code orchestrates everything; all process documents are portable markdown |
| Models | Per-role: Claude (subscription) for the judgment roles — Architect, Reviewer, Arbiter, Analyst, Planner, Retro; open Qwen3-Coder & Devstral (Apache 2.0) on a local DGX Spark via vLLM for the volume roles — Coder, Test Engineer, Doc writer |
| Routing | LiteLLM (on a Docker server) routes non-Claude models only — Claude is never metered per token |
| Gates | Risk-tiered (High/Standard/Low); humans can veto anywhere; branch protection — a GitHub setting that physically blocks merging until required checks pass — enforces it |
| Tests-first | Enforced by the red-proof CI job + role-separation hooks; 80% / 90% coverage; mutation testing on high-risk changes |
| Review | Claude reviewer as a GitHub Action (a different model family than the coder, on purpose) + Arbiter triage; 2-cycle cap |
| Autonomy | A dial, not a leap: Watched → Attended → Resident (headless on the Docker server) |
| Hermes Agent | Optional module: sovereign (fully-local) profile + Telegram notification bridge (backlog) |
| Product | Open-core; first market: SMB internal tools |

> **Software Engineering Validation:** Spec-driven and test-driven by construction — BDD-style acceptance criteria, ADRs with recorded alternatives, mechanically-enforced TDD (the red proof: CI verifies new tests fail on base and pass on head), generated requirements-traceability matrices, coverage gates (80% project / 90% changed lines), mutation testing scoped to `risk:high`, cross-model review, and risk-tiered phase gates backed by branch protection. Every gate is a PR approval; the audit trail is the Git history itself. Proof metrics lead with DORA.
