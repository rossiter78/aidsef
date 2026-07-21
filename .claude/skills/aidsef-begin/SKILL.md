---
name: aidsef-begin
description: One-time setup for a new project cloned from the AIDSEF template. Reads a short interview with you. Produces the trimmed, project-specific repo (its own README and CLAUDE.md, framework-authoring files removed) plus a single setup pull request whose approval adopts your constitution (Phase 0).
argument-hint: [project-name]
disable-model-invocation: true
---

# /aidsef-begin — set up your new project (run once)

Read `constitution.md` first, then run this **once**, right after you clone your new project from the template. It turns the template copy into *your* project. You stay in the loop the whole way — and a couple of steps only you can do (in the browser), where the skill will pause and tell you exactly what to click.

You act as the **organizer** here; there is no separate role to delegate to. Do the Git and file work yourself (the human never needs a terminal). Pause for the two browser steps — and never attempt those two yourself.

Project name (used in the drafts and the PR title): `$ARGUMENTS` — if empty, ask for one.

## Before this runs (the README covers these)

These happen *before* the skill can exist locally, so the template's `README.md` walks a new user through them: (1) on the template's GitHub page, **Use this template → Create a new repository**; (2) `git clone` the new repo and open it in Claude Code. **Guard:** if this folder *is* the AIDSEF template itself (its `origin` remote points at the `aidsef` template repo), stop and say so — `/aidsef-begin` is for a fresh project copy, not the template.

## Steps

1. **Interview the human** — a few small questions, not a giant form:
   - What is the project, in one or two sentences?
   - Any hard rules for the agents? (For example: data that must never enter the repository, or product-scope limits.)
   - Do you already have planning documents — a plan, research, prior specs? If so, we'll place them in `project/inputs/` so the Analyst and Architect read them.
   - Solo or team? (Solo is the default, and right for a first project.)
   - Any quality-threshold changes? (Default: keep the constitution's defaults.)

2. **Clean out the framework-authoring files** — they document how AIDSEF *itself* was built and don't belong in your project. Delete:
   - `docs/playbook/` (the whole folder)
   - `docs/00-getting-started.md` (the framework build-order guide)
   - the framework's own decision records: every `docs/adr/NNN-*.md` file — **keep `docs/adr/README.md`**, because your project writes its *own* ADRs here, starting fresh at `001`
   - empty out `BACKLOG.md` to a ready-to-use list (a heading and one line of guidance, no items)

   **Keep everything else:** `constitution.md`, all of `.claude/` (the lifecycle skills — and this one, so you can re-run setup if you ever want to start over), `.github/`, `docs/glossary.md`, `docs/adr/README.md`, `scripts/`, `tools/`, `tests/`, `specs/`, `retros/`, `project/inputs/`.

3. **Write the project's own `README.md` and `CLAUDE.md`**, replacing the template's (its `CLAUDE.md` describes building AIDSEF and would misdirect your agents). Draft both from the interview, then show the human and revise until they're happy. A project `CLAUDE.md` needs at least: what the project is, in two sentences; the line "**read `constitution.md` before starting any task**"; a pointer to the plan document (if any) and how binding it is; and the hard rules from the interview. The `README.md` describes the app for people.
   - If the human has planning documents (from step 1), have them drop those files into `project/inputs/` now, so they land in this same setup PR.

4. **⏸ Hand off the two browser-only steps — do NOT attempt these yourself; you cannot, and must not try.** These are the one part of setup only the human can do, and both must be finished *before* the pull request, or the AI code reviewer can't run on it. Explain that plainly, then give the human these two tasks and wait until they confirm both are done:
   - **Give the automation permission to use your Claude subscription.** In the new repo on GitHub: **Settings → Secrets and variables → Actions → New repository secret**; name it `CLAUDE_CODE_OAUTH_TOKEN`, and paste the value that `claude setup-token` prints (a one-time login you run once). This is what lets the GitHub review run on your Claude plan instead of a pay-per-use key. It's a password-like value, which is why only you can enter it.
   - **Let the Claude review app see this repository.** Go to [github.com/settings/installations](https://github.com/settings/installations), open the **Claude** GitHub App, and grant it access to your new repo.
   Tell the human these are one-time, and that you'll pick right back up the moment they say both are done.

5. **Run the setup script** — `bash scripts/setup-repo.sh` from the repo folder: it creates the labels, the Projects board, and branch protection. On a Free-plan private repo the branch-protection calls warn instead of succeeding — that's the known advisory-gates trade-off, not an error.

6. **Open the single setup pull request.** On a branch (e.g. `chore/project-setup`), commit: the trim (step 2), the new `README.md`/`CLAUDE.md` (step 3), any `project/inputs/` documents, and any constitution tuning the human chose (operating profile, threshold changes, project-specific law). Push, then `gh pr create` titled `Set up <project>`, labelled `risk:standard`, with a body summarizing what it does. **Approving and merging this one PR is Phase 0 — it adopts your constitution.** Say that plainly; the approval is the whole ceremony (there is no separate ratification form — Git records who adopted it and when).

7. **Announce and point the way.** Tell the human: the setup PR is open; approving it adopts the rulebook and finishes setup; after it merges, run `/aidsef-1-spec` to describe the first feature. Any planning documents now live in `project/inputs/` for the Analyst and Architect to read.

## Rules

- The two browser steps (step 4) are yours to *instruct*, never to perform — you cannot add a secret or grant app access, and must not try. Wait for the human.
- Everything lands via the one setup PR — even setup has an audit trail from commit one.
- Blocked or uncertain → open a `needs-human` issue and stop; never guess.
- Run once per project. The skill is kept (not deleted), so you can re-run setup if you ever want to start over.
