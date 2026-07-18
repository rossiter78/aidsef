# AIDSEF — project context for Claude Code

This repo is the **AIDSEF template repo in progress** (AI-Driven Software Engineering Framework). Design is complete; we are now building the framework's own files.

**Every agent, in every session: read [`constitution.md`](constitution.md) before starting any task.** It is the project rulebook — risk tiers, gates, quality thresholds, role separation, and escalation policy all live there. In projects cloned from this template, the ratified constitution is the supreme process authority; this file only points to it.

## Read before working
- `README.md` — all core decisions at a glance
- `docs/00-getting-started.md` — the build order (Phases A–D). **Current status: Phase A not started; all docs rewritten for the two-audience pattern (plain-language main text + "Software Engineering Validation" callouts + `docs/glossary.md`) on 2026-07-18.**
- `docs/playbook/01–06` — the authoritative design. When building any file, the matching playbook section is the spec:
  - Constitution → playbook 01 · Role charters → playbook 02 · LiteLLM config & workflows wiring → playbook 03 · Hooks, red-proof, CI → playbook 04 · Templates/labels/board → playbook 05 · License/open-core choices → playbook 06

## Non-negotiable decisions (do not re-litigate)
- Claude models are used via **subscription only** — never route Claude through LiteLLM, never per-token API keys except as documented escape valves. GitHub Actions use `CLAUDE_CODE_OAUTH_TOKEN`.
- LiteLLM (on the user's Docker server) routes **only** non-Claude models (Qwen3-Coder / Devstral on the DGX Spark via vLLM; Spark is inference-only).
- Local→cloud Coder escalation always requires **human approval** (`needs-human` issue).
- Humans never need a terminal; agents do all Git/CLI work.
- The repo is **open-core public**; keep it client-presentable.

## Audience — write for non-engineers first
The primary user of this repo is **not a software engineer**: they are someone who wants to build software with AI *responsibly* — and who must win over the skeptical software engineers around them. AIDSEF is "legitimized vibe coding" (never call it that publicly; the professional name is the point). Therefore:
- Every doc, charter, skill, and error message must be understandable by a smart non-engineer. Define engineering terms in plain language on first use (e.g., "branch protection — a GitHub setting that physically blocks merging code until required checks pass").
- The skeptical professional engineer is the **secondary** reader, served by **"Software Engineering Validation"** blockquote callouts that deliberately keep the precise jargon (TDD, BDD, ADRs, DORA, etc.).
- Users should *learn* proper software engineering by using the repo — docs teach as they instruct. `docs/glossary.md` defines every technical term in plain language; link terms to it on first use.

## Conventions
- All process artifacts are plain portable markdown.
- Deferred ideas go in `BACKLOG.md`, not into scope.
- Uncertain or blocked → ask the user; don't guess (the framework's own rule applies to building it).

## Phase A ground rules
- **Public from day one** — the repo history is a marketing asset; write every commit as if a skeptic will read it (they will).
- **Placeholders only** — never commit personal hostnames, machine names, or tokens. Ship `.env.example` + `http://YOUR-INFERENCE-HOST:8000`-style placeholders; real values live in untracked `.env` and GitHub secrets.
- **PRs only, even solo** — Phase A work lands via feature branches and pull requests, so the template's own history demonstrates the methodology.
- **Machinery tests happen in a scratch repo** — deliberately-broken PRs (Phase C) never pollute the template's history.

## Phase A deliverables (from docs/00-getting-started.md)
`constitution.md` · 9 charters in `.claude/agents/` · skills `/aidsef:spec|design|plan|build|retro` · hooks in `.claude/settings.json` · workflows `ci.yml`, `red-proof.yml`, `claude-review.yml`, `claude-fix.yml`, `resident-*.yml` (disabled) · issue/PR templates · `setup-repo` script (labels, branch protection, Projects board).
