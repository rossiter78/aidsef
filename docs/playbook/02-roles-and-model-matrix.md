# AIDSEF — Roles & model matrix

> Section 2 of the AIDSEF playbook. Decided 2026-07-18.
> Core principle: **roles are stable, models are configuration.**
> Each role is a written job description plus a pointer to whichever AI model currently fills the job. Swapping the model behind a role is a one-line configuration change; nothing about the process changes.

## 1. Role charters (summary)

AIDSEF runs on nine specialist AI roles — think of a small, disciplined team where every member has a written job description and hard limits on what they may touch. Each **[charter](../glossary.md#charter)** lives in `.claude/agents/<role>.md` and states: the mission, what the role receives, what it produces, its hard limits (what it may NOT do), and the [model alias](../glossary.md#model-alias) it runs on.

| Role | Mission | May not |
|---|---|---|
| **Analyst** | Interview you about what you want; produce `spec.md` with testable [Given/When/Then](../glossary.md#givenwhenthen) acceptance criteria | Invent requirements no human confirmed |
| **Architect** | Produce `design.md` + [ADRs](../glossary.md#adr-architecture-decision-record) recording alternatives and trade-offs | Write implementation code |
| **Planner** | Break the design into small, ordered GitHub Issues; stamp risk-tier labels | Merge or approve anything |
| **Test Engineer** | Write failing tests from the acceptance criteria; commit them before any product code exists | Modify implementation code |
| **Coder** | Make the tests pass; clean up; self-review; open the pull request | Edit tests to make them pass; touch files outside the task's scope |
| **Reviewer (AI)** | Review pull requests against the constitution + design; file categorized critiques | Approve its own fixes |
| **Arbiter** | Classify each critique (blocking / fix-now / deferred / rejected) with written reasoning | Override a human's classification |
| **Retro agent** | Mine each feature's history; propose rulebook/charter amendments via pull request | Merge its own amendments |
| **Doc writer** | Keep documentation in sync with merged changes | Alter code or tests |

The "may not" column is not a suggestion — it is enforced by machinery ([hooks](../glossary.md#hook) that physically block the wrong role from editing the wrong files; playbook §4).

## 2. Model matrix (defaults)

Which AI model fills each job. "Frontier cloud" means the most capable (and most expensive) commercial models; "local" means open models running on your own hardware, where extra usage costs nothing.

| Role | Alias | Model class | Default model | Runs on |
|---|---|---|---|---|
| Analyst | `analyst` | Frontier-lite cloud | Claude Sonnet 5 | Anthropic API |
| Architect | `architect` | Frontier cloud | Claude Fable 5 / Opus 4.8 | Anthropic API |
| Planner | `planner` | Frontier-lite cloud | Claude Sonnet 5 | Anthropic API |
| Test Engineer | `testwriter` | Local | Qwen3.6-35B-A3B | DGX Spark |
| Coder | `coder` | Local | Qwen3.6-35B-A3B | DGX Spark |
| Coder (escalation) | `coder-escalated` | Frontier cloud | Claude Sonnet 5 | Anthropic API |
| Reviewer | `reviewer` | Frontier cloud | Claude Fable 5 / Opus 4.8 | Anthropic API (GitHub Action) |
| Arbiter | `arbiter` | Frontier cloud | Claude Fable 5 / Opus 4.8 | Anthropic API |
| Retro | `retro` | Frontier-lite cloud | Claude Sonnet 5 | Anthropic API |
| Doc writer | `docwriter` | Local | Qwen3.6-35B-A3B | DGX Spark |

All three local roles share one model — Qwen3.6-35B-A3B, an agentic-coding release that superseded the originally-planned Qwen3-Coder 80B-A3B (see [ADR-001](../adr/001-local-model-qwen36-35b-a3b.md) for the decision and alternatives, including Devstral 2 as the documented fallback). Because roles are aliases, splitting them across models later is a one-line routing change.

Licensing note: Qwen3.6 (like Qwen3-Coder and Devstral 2 before it) is released under the [Apache 2.0 license](../glossary.md#apache-20-license) — free for commercial use, which matters if you resell AIDSEF-built software or the framework itself.

## 3. Principles

1. **The reviewer is never the author's twin.** The AI that reviews code must come from a different model family than the AI that wrote it (default: Claude reviews Qwen's code). Two copies of the same model share the same blind spots — this is the AI version of the rule that you don't review your own code.

   > **Software Engineering Validation:** Cross-model review as a structural control against correlated failure modes. The independence holds regardless of cloud-vendor choices, because the Coder is always a locally-hosted open-weight model from a different lineage than the frontier reviewer.

2. **Judgment goes up, volume goes down.** The most capable (expensive) models take the small-volume, high-consequence work: architecture, review, triage. The local models on your own hardware take the high-volume, well-specified work: code, tests, documentation. The Coder burns 10–50× the Architect's [tokens](../glossary.md#token) — on hardware you already own, where that costs nothing extra.

3. **Escalation needs a human's yes.** When the local Coder can't get the tests passing after N attempts (default 3), it stops and opens a `needs-human` issue summarizing what it tried and its diagnosis: is this beyond the local model's ability, or is the task itself badly specified? A human approves with one click or comment (`escalate` → the task re-runs on the frontier model; approvals can be batched) or re-scopes the task instead. Every escalation request and outcome is counted in the retros: a local model that escalates constantly isn't earning its slot, and if the diagnosis is repeatedly "the task was badly specified," that indicts the Planner instead.

4. **Cloud strategy: Anthropic-primary, multi-ready.** All cloud roles default to Claude — one billing relationship, native to the orchestration tool. But every role is just an alias in the routing layer, repointable to another vendor in one line; cross-model review holds regardless, because the Coder is local Qwen.

5. **AI review runs as a GitHub Action** — an automated job on GitHub that reviews every pull request against the constitution and design documents, and doubles as the fix-iteration engine (mention `@claude` on a pull request and it acts on the feedback). No per-seat software fee, and the review prompts are tunable by the retro loop.

   > **Software Engineering Validation:** The Claude-reviewer GitHub Action is the default stack; commercial reviewers (Greptile, CodeRabbit) slot in as an optional *second* reviewer for client engagements wanting defense-in-depth. Escalation telemetry (rate, hypothesis distribution) feeds the retro loop as a model-fitness and decomposition-quality signal.
