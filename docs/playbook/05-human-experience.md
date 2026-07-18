# AIDSEF — Human experience layer

> Section 5 of the AIDSEF playbook. Decided 2026-07-18.
> Guarantee: **agents use terminals; humans never do.** Every human interaction is chat, review, or click-approve.

## 1. Surface map

Everything you will ever do in AIDSEF, and where you do it. No command line, ever — the agents handle all the [Git](../glossary.md#git) and terminal work.

| Human action | Surface |
|---|---|
| Start a feature / answer the Analyst's questions | Claude Desktop (or VS Code chat) |
| Approve a spec / design | GitHub website or VS Code pull-request view (read the document, click Approve) |
| Watch the build loop (autonomy Levels 0–1) | VS Code Claude Code panel |
| Review code / overrule an Arbiter triage call | GitHub website / VS Code pull-request view (just reply — a human reply reclassifies a finding) |
| Approve an escalation | GitHub [issue](../glossary.md#issue): comment `escalate` / `re-scope`, or click a label |
| Monitor non-Claude AI spend | LiteLLM dashboard (in the browser) |
| Track task states | GitHub Projects board: `ready → building → in-review → needs-human → merged` |
| Notifications | GitHub notifications + GitHub Mobile (see backlog for the Hermes→Telegram bridge) |

## 2. Adoption notes

- **For client engineers, the human interface of AIDSEF is GitHub itself.** Reviewing an AIDSEF pull request is identical to reviewing a colleague's — zero new tooling for the skeptical reviewer to learn.
- **GitHub Mobile is a first-class approval surface** — at autonomy Level 2, gate approvals work from a phone.

## 3. GitHub plan requirements

**Decision: stay on the GitHub Free plan.** Private repositories are free and unlimited; the one Free-plan limitation that touches AIDSEF is that [branch protection](../glossary.md#branch-protection) — the setting that physically blocks the merge button until required checks pass — **is not enforced on private repos** (it is on public ones).

| Scenario | Cost | Notes |
|---|---|---|
| Public repos (template, dogfood/case-study projects) | $0 | Unlimited Actions minutes, branch protection fully enforced |
| Private repos, personal | $0 | All checks (CI, red-proof, AI review) still run and show ✗/✓ on the pull request, but GitHub will not physically block the merge button — the merge gate is **advisory, not mechanical**. Acceptable at solo scale: there is one merger, and the gates are in plain sight |
| Upgrade trigger | GitHub Pro $4/mo | Flip only when a private repo gains a second merger, or a demo requires showing mechanically unbypassable gates on a private repo. Pro also adds 3,000 Actions minutes/month |
| Client orgs | Their existing Team/Enterprise plan | Protection + minutes already included — client work unaffected |
| Actions minutes on private repos | $0 | The Free cap is 2,000 minutes/month; a [self-hosted runner](../glossary.md#self-hosted-runner) on the Docker server (Level 2) sidesteps it — self-hosted minutes are always free |

> **Software Engineering Validation:** The "mechanically unbypassable merge gate" claim holds on public repos and on any paid plan; on Free-plan private repos, required status checks report but do not block, so the gate is visible-but-advisory. State this honestly when presenting — the audit trail (checks, reviews, red proof) is intact either way; only the physical block on the merge button differs.

## 4. A day at autonomy Level 2 (solo profile)

- **8:30** — Queue review: the overnight run merged the standard-tier pull requests; one high-risk PR awaits your review; one escalation request sits with the Coder's own diagnosis of why it failed. You review the PR in VS Code and reply `re-scope` to the escalation (the Planner splits the task into smaller pieces).
- **11:00** — New feature: a ~20-minute Analyst conversation in Claude Desktop → spec pull request → approve after one revision.
- **17:30** — Approve the design PR (read the decision records, challenge one dependency, the Architect revises). The factory has its night's work.
