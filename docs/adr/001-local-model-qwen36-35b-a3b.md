# 001. Qwen3.6-35B-A3B as the single local model

- Status: accepted
- Date: 2026-07-18
- Feature: framework (Phase B — local model plane)

## Context

The playbook's model matrix (playbook §2) originally named Qwen3-Coder 80B-A3B for the Coder role and Qwen3-Coder / Devstral 2 for the Test Engineer — the strongest open-weight coding models at design time. Before Phase B began, Alibaba released Qwen3.6-35B-A3B (April 2026, Apache 2.0): a sparse mixture-of-experts model — 35B total parameters, only 3B active per token — tuned specifically for agentic coding, and it was already loaded and serving on the project's DGX Spark via vLLM.

The requirements the local model must meet, in priority order:

1. **Apache 2.0 license** — free commercial use underpins the open-core resale story.
2. **Agentic coding capability** — the Coder runs as a headless Claude Code agent making failing tests pass; terminal/agent benchmarks matter more than raw code-completion scores.
3. **Reliable structured tool calling through vLLM** — the whole local plane fails silently without it.
4. **Fits and runs fast on a single DGX Spark** — this is the high-volume, zero-marginal-cost tier.

## Decision

**Qwen3.6-35B-A3B (FP8) is the default model for all three local roles** — Coder, Test Engineer, and Doc writer. All three LiteLLM aliases (`coder`, `testwriter`, `docwriter`) point at the same vLLM deployment.

The vLLM server registers the model under the deployment name **`qwen36-35b-a3b-fp8-262k`** (set via `--served-model-name`), and `litellm/config.yaml` must reference that name — not the Hugging Face ID. Tool calling requires vLLM ≥ 0.19.0 with `--tool-call-parser qwen3_xml --enable-auto-tool-choice`.

## Alternatives considered

- **Qwen3-Coder 80B-A3B (the original pick).** Lost on recency: Qwen3.6-35B-A3B is two generations newer, scores markedly higher on the agentic benchmarks that match the Coder's actual job (SWE-bench Verified 73.4, Terminal-Bench 2.0 51.5), uses less memory, and generates faster (3B active parameters). Same license.
- **Devstral 2 as a separate Test Engineer model.** Deferred, not rejected. Running one model keeps the Spark simple and its memory free for long-context KV cache; the role charters are aliases, so a second model is a config change, not a redesign. Devstral remains the documented fallback if Qwen3.6's tool calling proves unreliable through the Claude Code → LiteLLM → vLLM chain.
- **A larger frontier-class open model.** Rejected: wouldn't fit the Spark alongside 262K-context KV cache, and the escalation path to Claude (constitution §7.3) already covers tasks beyond the local model's ability.

## Consequences

- **Easier:** one model to deploy, monitor, and version on the Spark; more memory available for the 262K context window; faster generation for the high-volume roles.
- **Harder / watch for:** all three local roles now share one model's blind spots. Cross-model review is unaffected — the constitution's rule (§4) is that the *Reviewer* comes from a different family than the Coder (Claude reviews Qwen's code) — but test-writer/coder diversity is gone until a second model earns its slot. Retro data on escalation rates will tell us if that matters.
- **Operational lesson, recorded for the smoke test:** during setup, the running container's config diverged from its `.env` file — Docker Compose's `environment:` block silently overrides `env_file:` values, and a config key that nothing consumes fails silently. The Phase B smoke test therefore verifies the *live endpoint* (`/v1/models`, plus a real tool-calling round-trip), never a config file.
