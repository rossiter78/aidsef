# Role charters

One file per AI role — its written job description. Each charter states the role's **mission**, what it **reads**, what it **produces**, its **hard limits** (what it may NOT do — enforced by hooks and CI, not honor), and the **model alias** it runs on. The full role/model matrix and the reasoning behind it live in [playbook §2](../../docs/playbook/02-roles-and-model-matrix.md).

| Charter | Lifecycle phase | Model class |
|---|---|---|
| [analyst](analyst.md) | 1 — Intake & spec | Frontier-lite cloud (Claude) |
| [architect](architect.md) | 2 — Architecture | Frontier cloud (Claude) |
| [planner](planner.md) | 3 — Task decomposition | Frontier-lite cloud (Claude) |
| [test-engineer](test-engineer.md) | 4 — TDD build loop (red) | Local (vLLM via LiteLLM) |
| [coder](coder.md) | 4 — TDD build loop (green) | Local (vLLM via LiteLLM) |
| [reviewer](reviewer.md) | 5 — Review | Frontier cloud (Claude, GitHub Action) |
| [arbiter](arbiter.md) | 5 — Triage | Frontier cloud (Claude) |
| [retro](retro.md) | 6 — Retrospective | Frontier-lite cloud (Claude) |
| [doc-writer](doc-writer.md) | Post-merge | Local (vLLM via LiteLLM) |

Swapping the model behind a role is configuration, not process change: cloud roles name a Claude model in their frontmatter; local roles are aliases resolved by [litellm/config.yaml](../../litellm/config.yaml).

Amending a charter follows constitution §8: pull request, human-approved, always.
