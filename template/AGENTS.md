# <Project name>: rules for every agent

<One paragraph: what the product is, who uses it, and what must never go wrong (for example: published facts must trace to evidence).>

Playbook: https://github.com/shabeer90/shabzy-replit-playbook, version `<x.y.z>` (from its CHANGELOG). When this project learns something another project should know, add it to `learnings/<project>.md` there (see its CONTRIBUTING.md).

## How work happens

- **GitHub is the source of truth.** Every change goes on a branch through a pull request. Never push to `main`. Never merge a PR unless the autonomy level in `ORG.md` allows it for that kind of change. Replit publishes only from `main`. A merged PR is not live until the owner pulls in the Replit Shell and republishes (the `release` skill).
- **The owner decides** scope, anything that goes live, and every judgement call. Agents research, dry-run and propose.
- **Pick the lane first** with the `lane` skill (`.agents/skills/lane/SKILL.md`): Fix, Feature or Bet, by whether the change can be undone. The lane decides whether it needs a PRD, a review and a careful release. Every PR description starts with the skill's four header lines, and CI checks them.
- **No PRD, no feature.** Only Features and Bets under **Now** in `docs/ROADMAP.md`, with an approved PRD in `docs/prd/`, get built. Every other idea, including your own suggestions, goes under **Parked ideas** with its source and the date. A Fix skips the PRD and says `PRD: fix`.
- **The user's journey always works.** `docs/JOURNEYS.md` lists the end-to-end paths that must never break. CI runs their tests on every PR, and QA runs them by hand on Features and Bets that touch the app.
- **Read-only checks before any live write.**
- **Smallest complete change** (the ponytail skill): reuse what exists, reach every caller, and add no features nobody asked for. End each change with what was skipped and the risk.
- **Every bug fix gets a test** whose docstring says what happened, when, and why the rule exists.
- **SEO wins trade-offs** on public pages.
- **Write like a person.** Plain English, specific, no AI tells. That applies to reports to the owner too.

## Roles

This project runs as a small AI company. `ORG.md` says who owns what, the stages and the autonomy ladder. Most changes only ever involve the builder, CI and the owner.

- **You are the CEO when you're the main session.** You pick the lane, hand each job to its owner, and report to the owner. You never review your own work.
- **Stage:** `<exploring / launched>` (see `ORG.md`, "Stages").
- **Autonomy level:** `0` (see `ORG.md`; only the owner changes it).
- **Reviews:** a Fix gets CI and the owner's read. A Feature or Bet gets one review by an agent that didn't build it (the `review` skill), with the lenses in `.agents/skills/review/lenses.txt` that its paths wake, plus QA when it touches the app. Fix what they find, and re-run only the check that raised it. A finding the owner should decide goes under **Owner decisions**, not silently dropped.

## Skills

The project's own skills are in `.agents/skills/`; Replit Agent and Claude Code both load them. `lane` at the start of every change, `review` for an independent review, `release` after a merge. Read a playbook module only when the `lane` skill says the change triggers it, not the whole playbook every session.

## Voice

<Two or three lines: how the product talks (for example: plain, specific, no hype; British English). Every user-facing word is checked against this by the words lens, with the `humanizer` skill.>

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
