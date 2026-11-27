# <Project name>

**Read `AGENTS.md` and `ORG.md` before doing anything.** They hold the rules for every agent working on this repo, including you. Replit reads `AGENTS.md` itself; this file is a second way in.

**Don't build features you suggest.** When you see something worth adding, add one line under **Parked ideas** in `docs/ROADMAP.md`, with the date and "Replit Agent". Only items under **Now**, with an approved PRD in `docs/prd/`, get built. A small fix is fine.

## How you change code

The guard hook in `.claude/hooks/` doesn't run for you, so these rules hold because you follow them. GitHub branch protection and CI are what enforce them.

1. Start every piece of work on a new branch from an up-to-date `main`. Never commit or push to `main`.
2. Before you push, run the same checks CI runs (`.github/workflows/pr-checks.yml`): types, tests, `pnpm build`, the bundle check, and the Playwright journeys against the built app. Fix what fails; don't skip or weaken a check to get green.
3. Never put a secret in a file. Secrets live in Replit's Secrets tool.
4. Open a pull request. In its description, link the PRD (or write `PRD: fix`), list what you changed and what you ran, and write "Built by Replit Agent. Reviews not run yet."
5. Don't write reviewer verdicts in `.reviews/`. The reviews are run by Claude Code on your branch, not by the agent that built it. Don't merge; the owner merges once reviews and CI pass.
6. For changes after review, push more commits to the same branch. Don't open a second PR.

## Publishing

Publish only from `main`, after the PR is merged. Run `git pull origin main` in the Shell first, and run the live check in `AGENTS.md` afterwards.
