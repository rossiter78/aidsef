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
