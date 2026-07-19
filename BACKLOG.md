# AIDSEF backlog

Enhancements deliberately deferred from v1. Each becomes a GitHub issue when the template repo goes live.

- **Hermes→Telegram notification bridge** — Hermes Agent (already Telegram-connected) polls GitHub for `needs-human` items and gate PRs, pushes instant Telegram pings. First real exercise of Hermes in its "optional module" lane; no core-loop changes.
- **Daily digest** — morning summary (merges, escalations, spend) as scheduled job posting an issue comment or email.
- **Self-hosted runner hardening guide + enablement (autonomy Level 2)** — dedicated user, containerized jobs, no fork-PR execution; workflow files ship disabled in v1.
- **AppFlowy mirror** — one-way sync of AIDSEF milestones onto the personal AppFlowy board.
- **Second AI reviewer (Greptile/CodeRabbit)** — defense-in-depth review tier for client engagements; Arbiter dedupes overlapping findings.
- **Hermes skill-distillation → retro loop** — feed Hermes-style learned skills into agent charters (v2 of the retrospective system).
- **Multi-vendor cloud demo** — repoint one role to a non-Anthropic cloud model as a vendor-independence demonstration for sales.
- **Nightly full-codebase mutation runs** — beyond high-risk-PR mutation checks; results feed retros.
- **Evals for non-deterministic components** — when a project's *product* includes an LLM feature, tests alone can't verify it: add an eval lane (labelled datasets, scoring rubrics, LM-judge checks in CI) alongside the test gates. Flagged by Google's [SDLC whitepaper](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding): without both tests *and* evals, it's still vibe coding. Needed before any dogfood project ships an AI feature.
- **First-pass success rate metric** — add "PRs merged with zero review-finding cycles" to the playbook §6.4 proof metrics; it directly demonstrates harness ROI (better context → first-try success) in client readouts.
- **Post-clone bootstrap** — a cloned project currently trims framework files and rewrites README/CLAUDE.md by hand (getting-started Phase D). Ship a `scripts/bootstrap-project.sh` (or first-run agent task) that does the trim, generates a project CLAUDE.md, and prompts for the constitution's ratification block — found while validating the clone UX for dogfood project #1.
