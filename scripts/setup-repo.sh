#!/usr/bin/env bash
# AIDSEF one-time repository setup (getting-started Phase A, step 7).
#
# Configures the GitHub side of a cloned AIDSEF project so a human
# never has to: the risk/workflow labels, branch protection with the
# required status checks, and a Projects board with the task-state
# columns. Safe to re-run - every step is idempotent.
#
# An agent runs this after cloning the template. Requires the GitHub
# CLI (`gh`) authenticated with repo + project scope
# (`gh auth login`, then `gh auth refresh -s project,read:project`).
#
# Usage: scripts/setup-repo.sh [owner/repo]
#   owner/repo defaults to the current repository.
set -euo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
OWNER="${REPO%%/*}"
echo "AIDSEF setup for: $REPO"

# --- Labels ----------------------------------------------------------------
# name|color|description
LABELS=(
  "risk:high|B60205|High-risk change: human gates armed at spec, design, and merge (constitution §3)"
  "risk:standard|FBCA04|Standard change: AI review + green checks; post-merge spot-check"
  "risk:low|0E8A16|Low-risk change: docs, tests-only, or small mechanical cleanup"
  "needs-human|D93F0B|Blocked or escalated: an agent needs a human decision (constitution §1.4)"
  "ready|1D76DB|Dependencies met: this task can be built now"
  "building|C5DEF5|Task is being built"
  "in-review|5319E7|Pull request open, under review/triage"
  "escalate|E99695|Approved to re-run on the frontier model (escalation)"
)
echo "Ensuring labels..."
for entry in "${LABELS[@]}"; do
  IFS='|' read -r name color desc <<< "$entry"
  gh label create "$name" --color "$color" --description "$desc" --repo "$REPO" 2>/dev/null \
    || gh label edit "$name" --color "$color" --description "$desc" --repo "$REPO" >/dev/null
  echo "  ✓ $name"
done

# --- Branch protection ------------------------------------------------------
# Requires the required status checks to pass and >=1 approving review
# before merging to main. On public repos / paid plans this is a hard
# block; on Free-plan private repos it reports but does not block
# (playbook §5.3) - the API call still succeeds where the plan allows it.
echo "Configuring branch protection on main..."
# The protection API requires real JSON types (booleans/integers/null),
# which `gh api -f` cannot send (it stringifies everything) - so we PUT
# an explicit JSON body instead.
if gh api -X PUT "repos/$REPO/branches/main/protection" \
  -H "Accept: application/vnd.github+json" \
  --input - >/dev/null 2>&1 <<'JSON'; then
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      { "context": "ci" },
      { "context": "red-proof" },
      { "context": "claude-review" }
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "restrictions": null
}
JSON
  echo "  ✓ required checks: ci, red-proof, claude-review; 1 approval required"
else
  echo "  ! branch protection not applied — expected on GitHub Free-plan PRIVATE repos"
  echo "    (checks still report on every PR; the merge block is advisory until you go public or upgrade — playbook §5.3)"
fi

# --- Projects board ---------------------------------------------------------
# Task-state board: ready → building → in-review → needs-human → merged.
echo "Ensuring Projects board 'AIDSEF'..."
if gh project list --owner "$OWNER" --format json --jq '.projects[].title' 2>/dev/null | grep -qx "AIDSEF"; then
  echo "  ✓ board 'AIDSEF' already exists"
else
  if gh project create --owner "$OWNER" --title "AIDSEF" >/dev/null 2>&1; then
    echo "  ✓ created board 'AIDSEF'"
    echo "    Add a single-select 'Status' field with options:"
    echo "    ready, building, in-review, needs-human, merged"
    echo "    (GitHub's API can't fully script custom field options yet — set them once in the UI.)"
  else
    echo "  ! could not create the board — run:  gh auth refresh -s project,read:project"
  fi
fi

echo "AIDSEF setup complete for $REPO."
