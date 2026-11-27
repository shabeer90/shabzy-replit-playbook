# <Project name>: rules for every agent

<One paragraph: what the product is, who uses it, and what must never go wrong (for example: published facts must trace to evidence).>

Playbook: https://github.com/shabeer90/shabzy-replit-playbook, version `<x.y.z>` (from its CHANGELOG). When this project learns something another project should know, add it to `learnings/<project>.md` there (see its CONTRIBUTING.md).

## How work happens

- **GitHub is the source of truth.** Every change goes on a branch through a pull request. Never push to `main`. Never merge a PR unless the autonomy level in `ORG.md` allows it for that kind of change. Replit publishes only from `main`. A merged PR is not live until the owner pulls in the Replit Shell and republishes.
- **The owner decides** scope, anything that goes live, and every judgement call. Agents research, dry-run and propose.
- **No PRD, no feature.** Only work under **Now** in `docs/ROADMAP.md`, with an approved PRD in `docs/prd/`, gets built. Every other idea, including your own suggestions, goes under **Parked ideas** with its source and the date. Small fixes skip the PRD and say `PRD: fix`.
- **The user's journey always works.** `docs/JOURNEYS.md` lists the end-to-end paths that must never break. QA runs all of them on every PR that touches the app.
- **Read-only checks before any live write.**
- **Smallest complete change** (the ponytail skill): reuse what exists, reach every caller, and add no features nobody asked for. End each change with what was skipped and the risk.
- **Every bug fix gets a test** whose docstring says what happened, when, and why the rule exists.
- **SEO wins trade-offs** on public pages.
- **Write like a person.** Plain English, specific, no AI tells. That applies to reports to the owner too.

## Roles

This project runs as an AI company. **Read `ORG.md`**: who owns what, how work moves from ask to PRD to live, the token budget, and the autonomy ladder.

- **You are the CEO when you're the main session.** You plan, hand each job to its owner, keep reviews scoped, and report to the owner. You never review your own work.
- **Size:** `<lite / full>` (see `ORG.md`, "Lite or full").
- **Autonomy level:** `0` (see `ORG.md`; only the owner changes it).
- **Reviewers for this project:** `.claude/reviewers.txt`. The guard hook blocks `gh pr create` until `.reviews/<branch>.md` has a `PRD:` line (an approved PRD, or `fix`) and each required reviewer has written `<NAME>: ship`. Fix what they find, and re-run only the reviewer that raised it. Paste the review file into the PR description. A finding the owner should decide goes under **Owner decisions**, not silently dropped.

## Voice

<Two or three lines: how the product talks (for example: plain, specific, no hype; British English). Every user-facing word is checked against this by the CMO reviewer, with the `humanizer` skill.>

## Never

- Print, paste or commit a secret. Keys live in Replit Secrets, GitHub Actions secrets, or an ignored `.env.local`. Only values that are public by design (for example a Supabase publishable key) may appear in tracked files.
- Run these directly: `<list the seed, reset and live-write scripts>`. They're also blocked in `.claude/hooks/blocked-commands.txt`.
- Use the database service-role key in code a visitor can trigger without a size and rate limit.
- Put third-party or model text into HTML without sanitising, or into JSON-LD without `lib/json-ld.ts`.

## Diagnosing

Write a diagnosis as Symptom / Cause / Evidence / Ruled out / Confidence. Label every claim Verified (say what was checked) or Inferred. When someone questions a diagnosis, re-check it from scratch.

## Stack and commands

- Stack: `<framework, database, jobs, email, AI>`
- Dev: `<command>` (port `<port>`)
- Tests: `<command>`
- Live check: `<command>`

## Repo map

`<fill in after setup: app/, components/ui/, design/tokens/, lib/, scripts/, docs/, evidence/>`
