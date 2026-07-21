# AIDSEF — Toolchain & interfaces

> Section 3 of the AIDSEF playbook. Decided 2026-07-18.

## 1. Physical architecture

The machines and software involved, and what runs where. Three boxes do the work: your laptop (where you talk to the AI), an AI inference machine (the NVIDIA DGX Spark, which runs the local models), and a small always-on server running [Docker](../glossary.md#docker) (which routes traffic and, later, hosts unattended runs).

| Component | Runs on | Notes |
|---|---|---|
| Claude Code (the [orchestrator](../glossary.md#orchestrator) and your main AI surface) | Windows laptop: VS Code extension + Claude Desktop | Interactive sessions; paid for by subscription, never per-use |
| [vLLM](../glossary.md#vllm) (the program that serves the local AI models) | **DGX Spark — [inference](../glossary.md#inference) only** | Serves Qwen3.6-35B-A3B on an OpenAI-compatible port; the Spark runs nothing else |
| [LiteLLM](../glossary.md#litellm) gateway (traffic router for AI requests) | **Dedicated Docker server** (container) | Routes ONLY non-Claude models; keeps the usage/spend records |
| Headless build-loop runner (autonomy Level 2) | Docker server | Disabled by default; see §4 |
| [GitHub Actions](../glossary.md#github-actions) (automated checks + AI review + `@claude` fix) | GitHub cloud runners | Claude signs in via `CLAUDE_CODE_OAUTH_TOKEN` (subscription), not a pay-per-use API key |
| Network | [Tailscale](../glossary.md#tailscale) private mesh | Laptop ↔ Docker server ↔ Spark; the identical pattern works at client sites |

## 2. Billing/auth model (important for the resale pitch too)

Two completely separate payment worlds, kept separate on purpose:

- **Claude never routes through LiteLLM.** Claude Code signs in with the Claude subscription directly (for interactive sessions) and via `claude setup-token` → a `CLAUDE_CODE_OAUTH_TOKEN` repository secret (for GitHub Actions). Cost: a flat subscription, no per-use meter.
  - Caveat: Actions usage shares the subscription's rate limits with your interactive sessions. Escape valve: put a pay-per-use API key into the review workflow *only*, if that ever becomes necessary.
- **LiteLLM routes only the non-Claude fleet:** the local models on the Spark, and any future third-party cloud models. LiteLLM's per-role budgets and logging double as cost telemetry — data for retros and for showing clients exactly what their AI spend was.
- The local model (Qwen3.6-35B-A3B; [ADR-001](../adr/001-local-model-qwen36-35b-a3b.md)) is Apache 2.0 — no licensing cost to run it.

> **Software Engineering Validation:** Subscription OAuth for all Claude surfaces (interactive + CI) keeps frontier-model cost flat and predictable; metered API keys exist only as a documented escape valve. LiteLLM provides alias-level routing, budgets, and spend telemetry for the open-weight fleet. This split is a deliberate architectural decision, not an accident of setup.

## 3. Interface contracts

How the pieces talk to each other — four connections, each with a defined contract:

1. **Claude Code ↔ models.** Cloud-role agents name Claude models directly. Local-role agents (coder, testwriter, docwriter) run as [headless](../glossary.md#headless) Claude Code invocations (no visible window) with `ANTHROPIC_BASE_URL` pointed at LiteLLM, which speaks the Anthropic messages format and translates to vLLM.
2. **LiteLLM ↔ backends.** `litellm/config.yaml` (stored in Git) maps each alias to its endpoint. The model name must match the vLLM server's `--served-model-name` exactly — verify against the live `/v1/models` endpoint, not a config file:

```yaml
model_list:
  - model_name: coder
    litellm_params:
      model: hosted_vllm/qwen36-35b-a3b-fp8-262k
      api_base: http://spark:8000/v1
  - model_name: testwriter
    litellm_params:
      model: hosted_vllm/qwen36-35b-a3b-fp8-262k
      api_base: http://spark:8000/v1
  # coder-escalated intentionally ABSENT: escalation goes to Claude via
  # subscription after human approval, not through the gateway
```

3. **Claude Code ↔ GitHub.** Agents use the Git command line and GitHub's `gh` tool; humans only ever see VS Code, Claude Desktop, and the GitHub website. A setup script configures [branch protection](../glossary.md#branch-protection): required checks (`ci`, `claude-review`) plus the approvals each risk tier demands.
4. **GitHub Actions ↔ Claude.** `claude-review.yml` reviews every pull request against the constitution + design docs; `claude-fix.yml` lets an `@claude` mention trigger a fix iteration. Both run on the subscription OAuth token.

## 4. Autonomy levels (trust is a dial, not a leap)

How much the AI does without you watching. Declared in `constitution.md`; this ladder is also the prescribed adoption path for client teams.

| Level | Name | Where the build loop runs | Your posture |
|---|---|---|---|
| 0 | Watched | Interactive Claude Code session, observed step-by-step | Learn the loop; verify the guardrails and gates actually fire |
| 1 | Attended | Unattended session on the laptop | Check in at the gates; interrupt at will |
| 2 | Resident | Headless on the Docker server, triggered by events or a schedule | Interact only via GitHub approvals and notifications |

What makes Level 2 safe: every human gate is **queueable**. An autonomous run never waits impatiently or guesses — it parks any blocked task as a `needs-human` item and moves on to the next unblocked task. The overnight pattern: approve specs and designs in the evening → standard-tier tasks are coded, reviewed, triaged, and merged by morning → high-risk pull requests and escalation requests wait politely in the queue for you.

Level 2 workflow files ship in the template **disabled**; enabling them is a configuration flag.

## 5. Hermes Agent positioning

Hermes is not in the core loop — one orchestrator keeps the system simpler, easier to debug, and easier to support. It is documented as the **sovereign profile**: a fully-local orchestration option for privacy-sensitive clients whose code and prompts may never leave the building (runs under WSL2 or on a Linux host). Its skill-distillation memory is a candidate enhancement for the retro loop in v2.

## 6. Template repo layout

What's in the box — the file layout every AIDSEF project starts from:

```
aidsef/
├── constitution.md                  # engineering rules incl. risk tiers, autonomy level
├── CLAUDE.md                        # points every agent at the constitution
├── .claude/
│   ├── agents/                      # one charter per role
│   ├── skills/                      # /aidsef-1-spec, /aidsef-2-design, /aidsef-3-plan, /aidsef-4-build, /aidsef-6-retro
│   └── settings.json                # hooks: TDD enforcement, test-on-edit
├── .github/
│   ├── workflows/ci.yml             # tests + coverage gate
│   ├── workflows/claude-review.yml  # AI reviewer on every PR (subscription OAuth)
│   ├── workflows/claude-fix.yml     # @claude mention → fix iteration
│   ├── workflows/resident-*.yml     # Level 2 runner workflows (disabled by default)
│   └── ISSUE_TEMPLATE/              # task template: acceptance criteria + risk tier
├── litellm/
│   ├── config.yaml                  # non-Claude aliases only
│   ├── docker-compose.yml           # gateway deployment
│   └── README.md                    # how to deploy it
├── specs/   docs/adr/   retros/
└── docs/playbook/                   # these six sections
```
