# Skills

Install community skills with the [Skills CLI](https://skills.sh), which records each skill in `skills-lock.json`:

```bash
npx skills add <github-owner/repo> --skill <name>
```

Every CLI-installed skill must be in `skills-lock.json`. Otherwise nobody can tell where a skill came from or whether it has changed. Replit's own guidance and Claude Code's built-in commands aren't installed this way, so they don't belong in the lockfile.

## Replit's built-in guidance and tools

Replit gives its Agent its own instructions and tools. They aren't skills from the Skills CLI, and a similar name doesn't make them the same thing. Before relying on one, check what the current session can actually do. A tool that worked last week, or a file that mentions it, doesn't prove it's available now. If a tool is missing, say what you used instead and what that left unchecked (see [review records](template/ORG.md#review-records)). Don't install a community skill just to fill the gap.

What one Replit environment offered (yours may differ, **check current docs**):

| Replit guidance | Used for | Owner | Check before using |
|---|---|---|---|
| Design | Design advice and frontend work | head-of-design | Can it render and test the result here? |
| App testing and browser tools | Running user journeys | qa-tester | Which browser tools and test runner work in this session? If you ran Playwright directly, say so. |
| Deployment | Release status and planning a release | CEO; the owner approves publishing | Read-only status only; looking isn't permission to publish |
| Workflows | Running the app's managed services | CEO | Use the existing managed service; don't start a second one |
| Database | Read-only checks on production data | head-of-data | Which database is it really pointed at? Replit's own database isn't your external one. |

Replit's docs: [App Testing](https://docs.replit.com/features/agent/app-testing), [Workflows](https://docs.replit.com/features/workspace-tools/workflows), [development and production databases](https://docs.replit.com/features/data-and-storage/development-and-production).

## Finding and adding skills

**Before starting a kind of task the project hasn't done before, check whether a skill already does it.**

1. **Search** with `find-skills` (vercel-labs/skills), installed in every project. It checks the [skills.sh](https://skills.sh/) leaderboard, then runs `npx skills find <query>`.
2. **Vet it before installing.** A skill is instructions and sometimes scripts that run with the agent's access.
   - Prefer well-known owners: anthropics, vercel-labs, mattpocock, supabase, cloudflare.
   - Read the whole `SKILL.md` and every script.
   - Reject anything that asks for credentials, posts or sends on your behalf, or fetches and runs remote code.
   - The owner approves each new skill.
3. **Install** with `npx skills add`, then check it's in `skills-lock.json` and add a row to this file.
4. **If nothing fits** and the task will happen again (twice is the signal), write a project skill with `skill-creator` (anthropics/skills). Use `writing-for-agents` (mattpocock/skills) to keep it short and clear.
5. **When a skill proves itself** on a project, add it here so the next project gets it on day one.

**One skill per job.** Each row below has one job, and its "Used by" column names the role that owns it (`template/ORG.md`). Before adding a skill, check the tables: if a skill already does the job, the new one must replace it (say why in the PR) or isn't added. Two skills for the same job means paying twice and getting conflicting advice.

## Every project

| Skill | Source | Used by | Job |
|---|---|---|---|
| find-skills | vercel-labs/skills | CEO | Finding an existing skill before a new kind of task (see above) |
| skill-creator | anthropics/skills | CEO | Writing a project skill when nothing fits |
| ponytail | local copy; record the source when installing | the builder | The smallest change that fully solves the task |
| caveman | juliusbrussee/caveman (core `caveman` skill only, pinned to a commit) | CEO, in chat | Shorter chat replies: answer first, no padding, code and errors exact. Written work (code, docs, commits, PRs, memory) stays in plain prose. Switch on with `/caveman`, off with `normal mode`. |
| humanizer | blader/humanizer | cmo-reviewer, and anyone writing for a person | Rewriting text so it reads like a person wrote it, with no AI tells |
| codebase-design | mattpocock/skills | cto-reviewer | Module and interface design |

## Products with a UI

| Skill | Source | Used by | Job |
|---|---|---|---|
| impeccable | pbakaus/impeccable | head-of-design | Design direction (`DESIGN.md`), craft and critique, so it looks agency-built, not AI-made. It ships scripts: read them before installing. |
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill | head-of-design | Palette, type-pairing and UX reference data |
| web-design-guidelines | vercel-labs/agent-skills | head-of-design | Accessibility and interface-guideline review |

## Product, review and QA (every project)

All were checked to exist in their repos on 27 Nov 2026. Read each SKILL.md before installing.

| Skill | Source | Used by | Job |
|---|---|---|---|
| webapp-testing | anthropics/skills | qa-tester | Drives the local app with Playwright: checks features, screenshots, browser logs |
| code-review (mattpocock) | mattpocock/skills | em-reviewer only | Reviews a diff against the PRD and the repo's standards, in parallel sub-agents |
| to-spec | mattpocock/skills | cpo | Turns a conversation into a first PRD draft |
| grilling | mattpocock/skills | cpo | Questions the owner one at a time until the ask is clear |
| tdd | mattpocock/skills | the builder | Red-green-refactor, so features arrive with tests |
| diagnosing-bugs | mattpocock/skills | CEO | A diagnosis loop for hard bugs, before guessing at a fix |

## When the project needs it

| Skill | Source | Used by | When |
|---|---|---|---|
| next-best-practices | vercel-labs/next-skills | the builder, cto-reviewer | Next.js projects |
| supabase-postgres-best-practices | supabase/agent-skills | head-of-data | Postgres or Supabase: schema, RLS, migrations |
| seo-audit | coreyhaines31/marketingskills | cmo-reviewer | Public sites: ranking and indexing |
| seo-geo | resciencelab/opc-skills | cmo-reviewer | Public sites: structured data, AI-search visibility |
| audit-website | squirrelscan/skills | cmo-reviewer, by owner decision | A full site crawl before launch and monthly after |
| security-audit | cloudflare/security-audit-skill | security-reviewer, by owner decision | Before launch and after big changes. Run on a read-only copy, outside the repo, with no network. Expensive: choose the depth first. |
| improve-codebase-architecture | mattpocock/skills | cto-reviewer, by owner decision | When the code has grown and needs restructuring |

## Working style (mattpocock/skills)

| Skill | Used by | Job |
|---|---|---|
| research | CEO | Investigating a question against primary sources and saving the findings in the repo |
| retro | CEO | The retrospective after each batch |
| writing-for-agents | CEO | Writing skills, `AGENTS.md` and `CLAUDE.md` that agents follow. `humanizer` is for text people read. |
| teach | owner | Learning a new area with a structured plan |

## Built into Claude Code (no install)

- `/code-review`: a bug pass on the current diff. cto-reviewer uses it; it's a different thing from mattpocock's `code-review` skill, which the EM uses.
- `/security-review`: a security pass on the branch. security-reviewer uses it.
- `/simplify`: cleanup without hunting bugs.

## Project skills

Write one with skill-creator when the project repeats a workflow with house rules. For example: Reddit replies drafted for manual posting, or a project's own release steps.

## Looked at, not chosen

So nobody re-evaluates these from scratch:
- **frontend-design (anthropics/skills):** a good, small design skill. `impeccable` covers the same job in more depth. Use it only if `impeccable` can't be installed.
- **stop-slop (hardikpandya/stop-slop):** the same job as `humanizer`, which is more detailed and maintained.
- **EveryInc compound-engineering `ce-code-review` and `ce-test-browser`:** a heavier multi-reviewer plugin that overlaps our own review agents.
- **Community "engineering-manager" skills on skills.sh:** these are about managing people, not reviewing features.
- **The Caveman CLI and its other features (juliusbrussee/caveman):** "Read less", "Auto", "Blocks", "Waste fixes" and "Browse" fail the vetting above:
  - the installer runs `npx ...@latest`;
  - it reconfigures every agent and login on the machine;
  - it sits between tools and the model;
  - "Auto" sends session data to their service once you sign in.

  Only the core `caveman` skill is used. By the repo's own measurement it's about 3% shorter than telling the agent "Answer concisely", so it's a style choice, not a big token saving.

