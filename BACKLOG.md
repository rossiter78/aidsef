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
- **`/aidsef-begin` onboarding skill** — automate new-project setup (getting-started Phase D steps 4–9): delete the framework-authoring files, draft the project `README.md`/`CLAUDE.md` from a short interview, walk the user through the two 👤 browser steps (OAuth secret, App access), run `setup-repo.sh`, then prompt for the ratification details (project name, ratifier, date, any threshold tuning or project-specific law) and open the bootstrap and ratification PRs. Found while running dogfood project #1's setup by hand — the steps existed only as chat guidance, which is exactly what a skill is for. (Supersedes the earlier "post-clone bootstrap script" idea: a skill can interview; a script can't.)
