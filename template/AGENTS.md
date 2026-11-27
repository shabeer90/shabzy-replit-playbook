# <Project name>: rules for every agent

<One paragraph: what the product is, who uses it, and what must never go wrong (for example: published facts must trace to evidence).>

Playbook: https://github.com/shabeer90/shabzy-replit-playbook. When this project learns something another project should know, add it to `learnings/<project>.md` there (see its CONTRIBUTING.md).

## How work happens

- **GitHub is the source of truth.** Every change goes on a branch through a pull request. Never push to `main`; never auto-merge. Replit pulls `main` and publishes. A merged PR is not live until the owner pulls in the Replit Shell and republishes.
- **The owner decides** scope, anything that goes live, and every judgement call. Agents research, dry-run and propose.
- **Read-only checks before any live write.**
- **Smallest complete change** (the ponytail skill): reuse what exists, reach every caller, and add no features nobody asked for. End each change with what was skipped and the risk.
- **Every bug fix gets a test** whose docstring says what happened, when, and why the rule exists.
- **SEO wins trade-offs** on public pages.

## Roles

- **head-of-data** (`.claude/agents/head-of-data.md`), for projects with a database or data pipelines: owns the schema file, access rules (RLS and grants), migrations, and every job that writes live data. Any schema or data change goes through it first.
- **head-of-design** (`.claude/agents/head-of-design.md`) owns `design/tokens/` and `components/ui/`. Pages and features use only those components and tokens. When a feature needs a component that doesn't exist, head-of-design adds it to `components/ui/` first. `scripts/check_design_system.py` enforces this in CI.
- **Reviews before every PR**, each by an agent that didn't write the code. The reviewers for this project are listed in `.claude/reviewers.txt`. Each writes its section and verdict in `.reviews/<branch>.md`, and the guard hook blocks `gh pr create` until every listed reviewer says `ship`.
  - **em-reviewer** (`.claude/agents/em-reviewer.md`): did we build what was asked, completely, with nothing extra, and is the handover clear?
  - **qa-tester** (`.claude/agents/qa-tester.md`): runs the feature like a user (edge cases, phone width, keyboard, errors) and adds an e2e test.
  - **cto-reviewer** (`.claude/agents/cto-reviewer.md`): correctness, the data rules below, and whether the change is the smallest that works.
  - **security-reviewer** (`.claude/agents/security-reviewer.md`): real trust-boundary failures, such as secrets, auth, injection, access rules, SSRF and abuse cost. On for every project.
  - **seo-geo-reviewer** (`.claude/agents/seo-geo-reviewer.md`), for public websites: findability by Google, Bing and AI assistants.
  - **head-of-data** as reviewer, for projects with a database: access rules, query correctness, safe writes, data quality, privacy.
- Fix what the reviews find, then re-run the reviewer that raised it. Paste the review file into the PR description. A finding the owner should decide goes under **Owner decisions**, not silently dropped.

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
