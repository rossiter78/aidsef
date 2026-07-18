# AIDSEF Glossary

Every technical term used in this repository, defined in plain language. This glossary is part of the product: using AIDSEF is meant to teach you real software engineering, and this is where the vocabulary lives. Terms link here on first use throughout the docs.

---

### Acceptance criteria
The specific, checkable conditions that must be true for a feature to count as "done." In AIDSEF they are written in [Given/When/Then](#givenwhenthen) form so each one can become a test.

### ADR (architecture decision record)
A short document recording one significant technical decision: what was decided, what alternatives were considered, and why they lost. Stored in `docs/adr/` so anyone can later ask "why is it built this way?" and get a real answer.

### Agent
An AI worker given a specific job, a set of tools, and written limits. AIDSEF uses nine of them (Analyst, Architect, Planner, Test Engineer, Coder, Reviewer, Arbiter, Retro, Doc writer), each defined by a [charter](#charter).

### Apache 2.0 license
A permissive open-source license: software under it can be used, modified, and sold commercially for free. The local model AIDSEF uses (Qwen3.6) carries this license.

### API (application programming interface)
The defined way one piece of software talks to another — its public "sockets." A *public API contract* is a promise other systems depend on, which is why changing one is always high-risk.

### Artifact
Any written work product the process creates and saves in [Git](#git): specs, designs, decision records, retros. In AIDSEF, if it isn't in Git, it didn't happen.

### Audit trail
A complete, tamper-evident record of who decided and changed what, when. In AIDSEF the audit trail is not a separate report — it *is* the repository history.

### Authentication / authorization (auth/authz)
Authentication: proving who you are (logging in). Authorization: what you're allowed to do once in (permissions). Changes touching either are automatically high-risk.

### Autonomy level
How much the AI does without you watching, on a 0–2 dial: **0 Watched** (you observe every step), **1 Attended** (it runs on your laptop; you check in at gates), **2 Resident** (it runs headless on a server; you interact only through GitHub approvals).

### BDD (behavior-driven development)
A practice where requirements are written as concrete examples of behavior ([Given/When/Then](#givenwhenthen)) that both humans and tests can read. AIDSEF's specs are BDD-style.

### Branch
A parallel line of work in [Git](#git) — a safe copy where changes are made and tested before being [merged](#merge) into the main version. AIDSEF gives every task its own branch.

### Branch protection
A GitHub setting that physically blocks merging code into the main branch until required checks pass and required approvals are given. It turns "please follow the process" into "the button won't work until you do."

### Charter
An agent's written job description: its mission, inputs, outputs, hard limits (what it may NOT do), and which model it runs on. One per role, in `.claude/agents/`.

### CI (continuous integration)
An automated system that runs your tests and checks on every proposed change, automatically. In AIDSEF, CI is what makes quality claims *verifiable*: the checks run whether or not anyone remembers to run them.

### Commit
One saved snapshot of changes in [Git](#git), with a message describing it. AIDSEF's build loop is a sequence of commits: failing tests first (red), then the code that makes them pass (green).

### Constitution
`constitution.md` — the project's rulebook of non-negotiable engineering rules (risk tiers, coverage thresholds, gate policy, autonomy level). Every agent reads it before every task; changing it requires a human-approved [pull request](#pull-request-pr).

### Coverage
The percentage of the code that is actually exercised by tests. AIDSEF's defaults: 80% of all lines, 90% of the lines changed in any pull request. High coverage alone can be gamed — see [mutation testing](#mutation-testing).

### Cross-model review
The rule that the AI reviewing code must come from a different model family than the AI that wrote it. Two copies of the same model share the same blind spots — the AI version of "you don't review your own code."

### Dependency
Third-party code your project builds on (libraries, packages). Adding one is high-risk by default, because you're importing someone else's code and its problems.

### Deployment
Putting software where its users can actually use it. *Deployment frequency* — how often you ship — is one of the [DORA metrics](#dora-metrics).

### Docker
Software that runs programs in **containers** — isolated, portable packages that behave the same on any machine. AIDSEF's routing gateway (LiteLLM) and Level-2 runner live in containers on a small always-on server.

### Dogfooding
Using your own product for your own real needs ("eating your own dog food"). AIDSEF's Phase D is a dogfood project: building a real tool with the framework to prove it works.

### DORA metrics
The software industry's standard yardstick for delivery performance, from the DevOps Research and Assessment program. Four numbers: deployment frequency (how often you ship), lead time for changes (idea-to-shipped time), change-failure rate (how often a change breaks something), and time-to-restore (how fast you recover).

### Escalation
What happens when the local Coder model can't finish a task after 3 attempts: it stops, opens a `needs-human` issue with its diagnosis, and waits. A human decides — retry on a stronger cloud model, or re-scope the task. Escalation never happens without a human's yes.

### Gate
A checkpoint where work stops until it's approved. AIDSEF's gates are [risk-tiered](#risk-tier): the riskier the change, the more gates require a human.

### Git
The version-control system that records every change to every file, forever, with author and timestamp. The foundation of AIDSEF's audit trail.

### GitHub
The website where Git repositories live, changes are reviewed, and AIDSEF's checkpoints happen. For AIDSEF humans, GitHub (plus VS Code and Claude Desktop) is the entire interface.

### GitHub Actions
GitHub's built-in automation: [workflows](#workflow) that run automatically on events like "a pull request was opened." AIDSEF's CI checks, red proof, and AI reviewer all run as Actions.

### Given/When/Then
The three-part template for writing a testable requirement: **Given** a starting situation, **When** something happens, **Then** this must be the result. Example: *Given a logged-out visitor, When they submit a valid email, Then an account is created.*

### Headless
Running a program with no visible window or interface — purely in the background. AIDSEF's local-model agents and Level-2 runner work headless.

### Hook
A rule wired into the AI's tooling that fires automatically on certain actions and can physically block them. Example: the hook that stops the Coder agent from ever editing a test file.

### Inference
Running an AI model to get answers (as opposed to training one). An *inference server* is a machine dedicated to that job — in AIDSEF, the DGX Spark.

### Issue
GitHub's unit of tracked work: a titled, numbered item that can be labeled, assigned, and discussed. AIDSEF's Planner turns designs into small ordered issues; agents open `needs-human` issues when blocked.

### KLOC
Thousand lines of code — a normalizing unit for metrics like "review findings per KLOC."

### Label
A colored tag on a GitHub issue or pull request (`risk:high`, `needs-human`, `ready`). In AIDSEF, labels carry real authority: changing a risk label re-tiers the work item and changes which gates arm.

### Lines of code (LOC)
A rough size measure for a change. AIDSEF uses it in risk triggers: over 400 changed lines is automatically high-risk; mechanical cleanups under 50 lines can qualify as low-risk.

### LiteLLM
An open-source gateway that receives AI requests and routes each one to the right model by alias, while logging usage and spend. In AIDSEF it routes **only** the non-Claude models.

### Merge
Folding a branch's finished changes into the main version of the code. In AIDSEF, merging is the moment guarded by [branch protection](#branch-protection).

### Mock
A stand-in object used in tests to replace something real (a database, a payment service). Useful — but a test can be "mocked into meaninglessness," testing nothing real; AIDSEF's reviewer checks for that.

### Model alias
A nickname (like `coder` or `reviewer`) that a role uses instead of a hard-coded model name. Repointing an alias to a different AI model is a one-line configuration change; the process doesn't change at all.

### Mutation testing
A check on the tests themselves: tooling deliberately introduces small bugs ("mutants") into the code and verifies the tests catch them. If a mutant survives, the tests weren't really testing. AIDSEF runs it on high-risk changes only, because it's computationally expensive.

### OAuth token
A revocable digital pass that lets software act on an account without holding its password. AIDSEF's GitHub automation uses a Claude subscription OAuth token (`CLAUDE_CODE_OAUTH_TOKEN`) instead of a pay-per-use API key.

### Open-core
A business model: the core product is free and public; services and premium modules are paid. AIDSEF's playbook and template are open; pilots, support, and premium modules are the paid layer.

### Open-weight model
An AI model whose trained parameters ("weights") are published, so anyone can run it on their own hardware. AIDSEF's Coder (Qwen3.6) is open-weight — no vendor can take it away or meter it.

### Orchestrator
The one program that coordinates all the agents, tools, and steps. In AIDSEF that is Claude Code; there is deliberately only one.

### PII (personally identifiable information)
Data that identifies a real person — names, emails, addresses, account numbers. Anything touching PII is automatically high-risk.

### Pull request (PR)
GitHub's mechanism for proposing changes: "here is a branch of finished work — review it, discuss it, and approve it before it merges." Every AIDSEF decision gate is a pull request, which is what makes the audit trail automatic.

### RACI
A standard chart of who is Responsible, Accountable, Consulted, and Informed for each decision. AIDSEF's solo and team profiles are the same process with different RACI assignments.

### Red proof
AIDSEF's signature check: CI verifies that a task's new tests **fail** against the code as it was (red), and **pass** with the change (green). Mechanical, re-runnable proof that tests came first and genuinely test the change. See playbook §4.

### Refactor
Improving code's structure without changing what it does — cleanup, not new behavior. The third step of the TDD rhythm: red, green, refactor.

### Repository (repo)
A project's complete home in Git: all files, all history, all discussion. "The repo" is both the codebase and its audit trail.

### Required status check
A CI check that GitHub is configured to require before a merge is allowed (via [branch protection](#branch-protection)). AIDSEF makes `ci`, `red-proof`, and `claude-review` required.

### Retrospective (retro)
A structured look back after finishing work: what recurred, what escaped, what humans had to override. AIDSEF's Retro agent writes one per feature and turns patterns into proposed rule changes — delivered as PRs a human approves.

### Risk tier
The High / Standard / Low label that says how dangerous a change could be, and therefore which gates require a human. Proposed by the Planner, overridable by any human with one label change.

### Self-hosted runner
Your own machine doing the work for GitHub Actions instead of GitHub's cloud computers. Minutes on your own hardware are always free.

### Smoke test
The simplest possible end-to-end check that a system is alive and wired correctly — named for "plug it in and see if smoke comes out."

### Spec (specification)
The written statement of *what* to build and how you'll know it's done, before any code exists. AIDSEF specs live in `specs/<feature>/spec.md` with numbered, testable acceptance criteria.

### Tailscale
Software that creates a private, encrypted network between your machines over the internet, as if they were on the same desk. Connects the laptop, Docker server, and Spark.

### TDD (test-driven development)
The practice of writing a failing test *before* writing the code that makes it pass. The rhythm is red (failing test) → green (make it pass) → refactor (clean up). AIDSEF enforces it mechanically via the [red proof](#red-proof) and role-separation [hooks](#hook).

### Token
The unit AI models read and produce text in — roughly three-quarters of a word. Cloud AI is usually billed per token; AIDSEF routes its high-token work to local models where tokens cost nothing extra.

### Traceability matrix
A generated table mapping every requirement to the test(s) that prove it. AIDSEF's CI regenerates it on every pull request and fails the PR if any requirement is uncovered — so nothing in the spec silently goes untested.

### Triage
Sorting review findings by what to do about them: `blocking`, `fix-now`, `deferred`, or `rejected` — each with written reasoning. Done by the Arbiter agent; any human reply overrides it.

### Vacuous test
A test that can't actually fail — it runs code but asserts nothing meaningful, inflating [coverage](#coverage) without adding safety. AIDSEF's reviewer explicitly hunts for these.

### vLLM
An open-source, high-performance program for serving AI models. Runs on the DGX Spark, exposing the local models on a standard (OpenAI-compatible) port.

### Workflow
An automation recipe for [GitHub Actions](#github-actions): a file describing what to run and when (e.g., "on every pull request, run the tests"). AIDSEF's live in `.github/workflows/`.

### WSL2
Windows Subsystem for Linux — a way to run Linux software inside Windows. Relevant for the fully-local sovereign profile.
