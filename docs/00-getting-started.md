# AIDSEF — Getting started: the build order

Concrete steps from "design on paper" to "building real software with AIDSEF." Phases A–C are one-time setup; Phase D is the first real project. Claude Code can execute nearly all of this; steps marked 👤 need you personally. Unfamiliar terms are defined in the [glossary](glossary.md).

## Phase A — Repo scaffold (~half a day, all doable in Claude Code)

Build the template repository — the starter kit every AIDSEF project will be cloned from.

1. 👤 Create the GitHub repository `aidsef` (public — open-core) and connect this directory to it (`git init`).
2. Write `constitution.md` — the project rulebook — from playbook §1 defaults (risk tiers, gate policy, coverage 80/90, autonomy level 0, solo profile).
3. Write the 9 role charters (agent job descriptions) in `.claude/agents/` from playbook §2: mission, inputs, outputs, hard limits, model alias.
4. Write the skills — reusable commands that drive each lifecycle phase: `/aidsef:spec`, `/aidsef:design`, `/aidsef:plan`, `/aidsef:build`, `/aidsef:retro` — each using the matching charter.
5. Write the hooks (rules that physically block agents from forbidden edits) in `.claude/settings.json`: Coder blocked from `tests/**`, Test Engineer blocked from `src/**`, tests auto-run after edits.
6. Write the automated workflows: `ci.yml` (tests + coverage + traceability check), `red-proof.yml`, `claude-review.yml`, `claude-fix.yml`, `resident-*.yml` (shipped disabled).
7. Write the issue/PR templates and a `setup-repo` script (labels: `risk:*`, `needs-human`, `ready`; branch protection; Projects board).
8. 👤 Run `claude setup-token`; add `CLAUDE_CODE_OAUTH_TOKEN` to the repository's Actions secrets — this lets the GitHub automation use your Claude subscription instead of a pay-per-use key.

## Phase B — Local model plane (~half a day)

Stand up the local AI models — the ones that run on your own hardware and cost nothing per use.

1. 👤 On the DGX Spark: run vLLM (the model-serving program) with Qwen3-Coder (and optionally Devstral 2) on port 8000. The Spark serves inference only — nothing else runs on it.
2. On the Docker server: run the LiteLLM container with `litellm/config.yaml` (aliases `coder`, `testwriter`, `docwriter` → the Spark, over the Tailscale private network). Enable spend logging.
3. Smoke test — the simplest possible end-to-end check: a headless Claude Code run with `ANTHROPIC_BASE_URL` pointed at LiteLLM; confirm a `coder`-alias request actually lands on the Spark.

## Phase C — Verify the machinery (1–2 hours)

Before trusting the guardrails, deliberately try to break them (in a scratch repo, not the template):

1. Open a deliberately bad pull request — implementation code with no tests → the red-proof check must fail it.
2. Open a good pull request → the red proof passes, the Claude reviewer files structured findings, the Arbiter triages them, and branch protection demands the human click.
3. Confirm a Coder session is genuinely blocked from editing a test file.

> **Software Engineering Validation:** This is an acceptance test of the governance layer itself — negative-path first. If the red proof can't fail a test-less PR, or the role-separation hook doesn't block, nothing downstream can be trusted; fix before Phase D.

## Phase D — Dogfood project #1

Use AIDSEF to build something real — "dogfooding" means using your own product for your own needs.

1. 👤 Pick a small real app you actually want (internal-tool-sized; it doubles as your first case study).
2. Clone the template into a new repository; ratify its constitution (5 minutes solo).
3. Run the full lifecycle at **autonomy Level 0** — watch everything: `/aidsef:spec` conversation → approve the spec PR → `/aidsef:design` → approve → `/aidsef:plan` → `/aidsef:build` task by task → review/triage → merge.
4. After the first feature: run `/aidsef:retro`; approve (or reject) its first amendment PR.
5. Weeks 2–3: move to Level 1 (attended). Level 2 (resident, on the Docker server) only when the retros say the loop has earned it.

## Trust milestones (when to turn the autonomy dial)

- **Level 0 → 1:** two consecutive features with zero red-proof failures and no surprise triage overrides.
- **Level 1 → 2:** escalation rate below 1 per 10 tasks, and you've stopped reading standard-tier changes line-by-line and started sampling them — the sign that the machinery, not vigilance, is carrying the trust.
