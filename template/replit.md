# <Project name>

**Read `AGENTS.md` before doing anything.** It holds the rules for every agent working on this repo, including you. Replit reads `AGENTS.md` itself; this file is a second way in.

**Use the project skills in `.agents/skills/`.** `lane` at the start of every change, `review` when asked to review someone else's branch, `release` after a merge.

**Don't build features you suggest.** When you see something worth adding, add one line under **Parked ideas** in `docs/ROADMAP.md`, with the date and "Replit Agent". Only Features and Bets under **Now**, with an approved PRD in `docs/prd/`, get built. A Fix is fine.

## How you change code

The guard hook in `.claude/hooks/` doesn't run for you, and nothing in this file is enforced by Replit. What does hold is GitHub: branch protection on `main` and the required CI checks.

1. Pick the lane with the `lane` skill. If it's a Feature or Bet with no approved PRD, stop and tell the owner.
2. Start on a new branch from an up-to-date `main`. Never commit or push to `main`.
3. Before you push, run the same checks CI runs (`.github/workflows/pr-checks.yml`): the secrets scan, types, `python scripts/check_design_system.py`, tests, `pnpm build`, the bundle check, `scripts/assert_new_tests_fail_on_base.sh origin/main`, and the Playwright journeys against the built app. Fix what fails; don't skip or weaken a check to get green.
4. Never put a secret in a file. Secrets live in Replit's Secrets tool.
5. Open a pull request whose description starts with the `lane` skill's four header lines, then what you changed and what you ran. For a Feature or Bet, add "Built by Replit Agent. Review not run yet."
6. Don't review your own branch, and don't write `.reviews/`. Don't merge; the owner merges once CI passes and, for a Feature or Bet, the review says ship.
7. For changes after review, push more commits to the same branch. Don't open a second PR.

## Publishing

Follow the `release` skill: publish only from a clean, up-to-date `main`, after the PR is merged. Never publish from a branch or with uncommitted changes in the workspace; the live-drift check will flag it.
