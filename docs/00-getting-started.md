# AIDSEF — Getting started: the build order

Concrete steps from "design on paper" to "building real software with AIDSEF." Phases A–C are one-time setup; Phase D is the first real project. Claude Code can execute nearly all of this; steps marked 👤 need you personally. Unfamiliar terms are defined in the [glossary](glossary.md).

## Phase A — Repo scaffold (~half a day, all doable in Claude Code)

Build the template repository — the starter kit every AIDSEF project will be cloned from.

1. 👤 Create the GitHub repository `aidsef` (public — open-core) and connect this directory to it (`git init`).
2. Write `constitution.md` — the project rulebook — from playbook §1 defaults (risk tiers, gate policy, coverage 80/90, autonomy level 0, solo profile).
3. Write the 9 role charters (agent job descriptions) in `.claude/agents/` from playbook §2: mission, inputs, outputs, hard limits, model alias.
4. Write the skills — reusable commands that drive each lifecycle phase: `/aidsef-spec`, `/aidsef-design`, `/aidsef-plan`, `/aidsef-build`, `/aidsef-retro` — each using the matching charter. (Hyphenated, not colon-namespaced: in Claude Code, a project skill's command name comes from its directory name, and colons are reserved for plugin namespaces.)
5. Write the hooks (rules that physically block agents from forbidden edits) in `.claude/settings.json`: Coder blocked from `tests/**`, Test Engineer blocked from `src/**`, tests auto-run after edits.
6. Write the automated workflows: `ci.yml` (tests + coverage + traceability check), `red-proof.yml`, `claude-review.yml`, `claude-fix.yml`, `resident-*.yml` (shipped disabled).
7. Write the issue/PR templates and a `setup-repo` script (labels: `risk:*`, `needs-human`, `ready`; branch protection; Projects board).
8. 👤 Run `claude setup-token`; add `CLAUDE_CODE_OAUTH_TOKEN` to the repository's Actions secrets — this lets the GitHub automation use your Claude subscription instead of a pay-per-use key.

## Phase B — Local model plane (~half a day)

Stand up the local AI models — the ones that run on your own hardware and cost nothing per use.

1. 👤 On the DGX Spark: run vLLM (the model-serving program) with Qwen3.6-35B-A3B on port 8000 (see [ADR-001](adr/001-local-model-qwen36-35b-a3b.md) for the model choice). Tool calling — the model's ability to run commands and edit files, which the whole build loop depends on — requires vLLM ≥ 0.19.0 started with `--tool-call-parser qwen3_xml --enable-auto-tool-choice`; without those flags it fails silently. The Spark serves inference only — nothing else runs on it.
2. Verify the *running server*, not its config files: `GET /v1/models` must list the exact model name `litellm/config.yaml` expects (the `--served-model-name`, not the Hugging Face ID). Config files describe intent; only the live endpoint is fact — during setup we caught a Docker Compose `environment:` block silently overriding the `.env` file.
3. 👤 On the Docker server: deploy the LiteLLM gateway — `docker compose up -d` in `litellm/`, which pulls the official image and mounts `litellm/config.yaml`. Full instructions in [`litellm/README.md`](../litellm/README.md). Confirm `GET /v1/models` on the gateway lists all three aliases (`coder`, `testwriter`, `docwriter`) before going further.

### The smoke test

The build loop rests entirely on **tool calling** — the model's ability to read files, edit them, and run commands. That capability crosses two translation boundaries (Claude Code's Anthropic format → LiteLLM → vLLM's OpenAI format), and the known failure mode is silent: the model emits its tool call as ordinary text and nothing errors, it just doesn't *do* anything. Test it deliberately, in three stages:

1. **vLLM alone.** Send a request directly to the Spark that cannot be answered without a tool. The reply must contain a structured `tool_calls` field. If the tool call appears as text inside the message body instead, the `--tool-call-parser` flag isn't working — fix that before anything else.
2. **The gateway handshake.** Point `ANTHROPIC_BASE_URL` at LiteLLM and start Claude Code. It calls `GET /v1/models` on startup and lists what it finds in its model picker, labelled "From gateway" — a free check that the two ends agree before you send real work.
3. **The full chain, ten times.** Run a headless Claude Code invocation against a task that *forces* tool use — "read this file, change this line, run the tests" — and confirm the edit actually happened on disk. Then **run it ten times and count the failures.** The known instability is intermittent, not absolute: a single pass proves the path exists, not that it's reliable enough to trust unattended. Ten clean runs is the result you want written down before the Coder gets real tasks.

> A test the model can pass without calling a tool proves nothing — it just doesn't exercise the thing being tested. Make the task impossible to complete without touching a file.

If failures appear, check the response body for tool-call syntax sitting in the message text: that fingerprint means the parser or the format translation is at fault, not the model's ability.

The first thing to try is turning off the model's **"thinking" output** — the private reasoning some models emit before their real answer. It is a plausible culprit because that extra text has to survive the same translation as the tool call. On the Spark, this is the `PRESERVE_THINKING` setting in the vLLM host's `.env` (set it to `0`, recreate the container, re-run the ten). If the failures persist, the documented fallback is a different local model ([ADR-001](adr/001-local-model-qwen36-35b-a3b.md)).

## Phase C — Verify the machinery (1–2 hours)

Before trusting the guardrails, deliberately try to break them (in a scratch repo, not the template):

1. Open a deliberately bad pull request — implementation code with no tests → the red-proof check must fail it.
2. Open a good pull request → the red proof passes, the Claude reviewer files structured findings, the Arbiter triages them, and branch protection demands the human click.
3. Confirm a Coder session is genuinely blocked from editing a test file.

> **Software Engineering Validation:** This is an acceptance test of the governance layer itself — negative-path first. If the red proof can't fail a test-less PR, or the role-separation hook doesn't block, nothing downstream can be trusted; fix before Phase D.

## Phase D — Dogfood project #1

Use AIDSEF to build something real — "dogfooding" means using your own product for your own needs. Steps 2–9 are the standard setup for **any** project cloned from the template; do them in this order, because the later ones depend on the earlier ones. (Backlog: a `/aidsef-begin` skill will automate steps 4–9.)

1. 👤 Pick a small real app you actually want (internal-tool-sized; it doubles as your first case study).
2. 👤 **Create the project repository from the template button.** On the [aidsef repo page](https://github.com/rossiter78/aidsef), click **Use this template → Create a new repository**; name it after your project; choose Private or Public (private on a Free plan makes the merge gates advisory rather than physically blocking — see playbook §5.3). This copies the files into a brand-new repository with a fresh history and **no link back to the template**. Do *not* `git clone` the template itself — that would drag along AIDSEF's own history and remote.
3. **Clone the *new* repository to your machine** — the project repo from step 2, not the template: `git clone https://github.com/YOUR-USER/YOUR-PROJECT.git` (or let an agent do it). Everything from here on happens inside that folder.
4. **Trim the framework-authoring files** — they document how AIDSEF itself was built and don't belong in your project: delete `docs/playbook/`, `docs/00-getting-started.md` (yes, this very file), and `BACKLOG.md` (start your own, empty). Keep everything else: `constitution.md`, `.claude/`, `.github/`, `docs/glossary.md`, `docs/adr/`, `scripts/`, `tools/`, `tests/`, `specs/`, `retros/`.
5. **Write the project's own `README.md` and `CLAUDE.md`** (replacing the template's — its `CLAUDE.md` describes building AIDSEF and would misdirect your agents). You are not expected to have these already; **ask the agent to draft them, then review** — that review is your first approval act on the project. A project `CLAUDE.md` needs at minimum: what the project is, in two sentences; "**read `constitution.md` before starting any task**"; a pointer to your plan document (if you have one) and how binding it is; and your hard rules (for example: what data may never enter the repository). The `README.md` describes the app for humans.
6. 👤 **Wire up the review machinery — this must happen *before* the first pull request**, or the AI review can't run on it. Two per-repository settings, both done in the browser: add the `CLAUDE_CODE_OAUTH_TOKEN` secret to the new repo (repo → Settings → Secrets and variables → Actions; the value comes from `claude setup-token`), and grant the Claude GitHub App access to the new repo at [github.com/settings/installations](https://github.com/settings/installations).
7. **Run `bash scripts/setup-repo.sh`** from the repo folder (an agent can do this for you): creates the labels, the Projects board, and branch protection. On a Free-plan private repo the branch-protection calls will warn instead of succeed — that's the known advisory-gates trade-off, not an error.
8. **Open the first pull request** (`chore` class): the trim from step 4 plus the new files from step 5, on a branch, through a PR. Even setup lands via pull request — the audit trail starts at commit one.
9. **Ratify the constitution — this is Phase 0, and merging the PR *is* the ratification.** Open `constitution.md`; fill in the ratification block at the top (project name, your name, today's date — the solo profile and autonomy level 0 defaults are already correct for a first project); tune the §3–§6 tables only if your project needs different thresholds; add any project-specific law (for example, data-handling rules or product scope caps). Land it as its own PR and approve it. **Your approval of that PR is the ratification ceremony — there is nothing else to do.**
10. **Run the full lifecycle at autonomy Level 0** — watch everything: `/aidsef-spec` conversation → approve the spec PR → `/aidsef-design` → approve → `/aidsef-plan` → `/aidsef-build` task by task → review/triage → merge. **Having a pre-written plan document does not skip these phases:** the traceability gate requires a spec with numbered `AC-###` criteria before product code can merge, so `/aidsef-spec` always runs. A good plan makes the conversations *short* — the Analyst starts from your plan instead of a blank page — but the spec still gets written and approved. **Put any pre-existing plans, research, or draft specs in `project/inputs/` before you start** — the Analyst and Architect read that folder automatically at the start of Phases 1 and 2, and cite what they used; your originals are never modified.
11. After the first feature: run `/aidsef-retro`; approve (or reject) its first amendment PR.
12. Weeks 2–3: move to Level 1 (attended). Level 2 (resident, on the Docker server) only when the retros say the loop has earned it.

## Trust milestones (when to turn the autonomy dial)

- **Level 0 → 1:** two consecutive features with zero red-proof failures and no surprise triage overrides.
- **Level 1 → 2:** escalation rate below 1 per 10 tasks, and you've stopped reading standard-tier changes line-by-line and started sampling them — the sign that the machinery, not vigilance, is carrying the trust.
