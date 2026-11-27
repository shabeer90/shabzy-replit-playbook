# Skills

Install community skills with the [Skills CLI](https://skills.sh), which records each skill in `skills-lock.json`:

```bash
npx skills add <github-owner/repo> --skill <name>
```

Every CLI-installed skill must be in `skills-lock.json`. On Cogniscore, 7 of 15 were missing, so nobody could tell where they came from or whether they had changed. Platform-managed guidance and Claude Code built-ins are separate sources, not missing lockfile entries.

For community skills, check the installed instructions and lockfile source before use. For Claude Code built-ins, check the current session's command list and permissions, not the Skills CLI. The owning roles below stay the same whichever environment runs the work.

## Replit-provided guidance and tools

Replit supplies instructions and tools to Agent in its task environment. Replit is the provider of those instructions; they are not community packages installed with the Skills CLI. Their names do not establish equivalence to community skills or Claude Code built-ins.

Before execution, read the guidance exposed to the current session and check which tools are actually callable, with what permissions. A file, role name or past successful run does not establish present tool access. If a tool is missing, record the substitute and uncovered checks using the [review handoff](template/ORG.md#review-records). Do not install an overlapping skill just to match a name.

These examples reflect Ihsan's environment, not a portable tool set or a guarantee for every Replit session:

| Replit-provided guidance | Purpose | Existing owning role | Execution-time availability check |
|---|---|---|---|
| Design | Design consultation and frontend work | head-of-design | Read current design instructions; check the supported consultation/delegation mode and whether it can render or test the result |
| Testing guidance and available browser tools | Exercise user journeys and capture evidence | qa-tester | Check current browser tools and test-runner access; report direct Playwright use as such, not as a specialized callback |
| Deployment | Inspect release status and plan an authorized release | CEO; owner approves publishing | Check current deployment guidance, read-only status access and release permissions; inspection is not permission to publish |
| Workflows | Run and inspect managed development services | CEO | Check the configured service/workflow and available start/status controls; reuse the managed service rather than launch a duplicate |
| Database investigation | Inspect production data without writes | head-of-data | Check database guidance, the actual target and supported read-only production access; managed-database access does not establish access to an external database |

Official references: [App Testing](https://docs.replit.com/features/agent/app-testing), [Workflows](https://docs.replit.com/features/workspace-tools/workflows) and [development and production databases](https://docs.replit.com/features/data-and-storage/development-and-production). Exact guidance, callbacks and permissions remain environment-specific: **(check current docs)**.

*On Ihsan:* earlier design consultation informed the plan. A later integrated review lacked specialized architecture/browser callbacks, so independent general workers assessed source and ran Playwright. Managed workflows and read-only release investigation supported that review; they did not establish signed-in production success.

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
| code-review | mattpocock/skills | em-reviewer | Reviews a diff against the PRD and the repo's standards, in parallel sub-agents |
| to-spec | mattpocock/skills | cpo | Turns a conversation into a written spec; the cpo puts it in the PRD template |
| grilling | mattpocock/skills | cpo | Questions the owner one at a time until the ask is clear |
| tdd | mattpocock/skills | the builder | Red-green-refactor, so features arrive with tests |
| diagnosing-bugs | mattpocock/skills | anyone | A diagnosis loop for hard bugs, before guessing at a fix |



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

- `/code-review`: review the current diff for bugs. cto-reviewer uses it.
- `/security-review`: a security pass on the branch. security-reviewer uses it.
- `/simplify`: cleanup without hunting bugs.

## Project skills

Write one with skill-creator when the project repeats a workflow with house rules. On Cogniscore these were Reddit replies drafted for manual posting, and releasing a brand's evidence.

## Looked at, not chosen

So nobody re-evaluates these from scratch:
- **frontend-design (anthropics/skills):** a good, small design skill. `impeccable` covers the same job in more depth. Use it only if `impeccable` can't be installed.
- **stop-slop (hardikpandya/stop-slop):** the same job as `humanizer`, which is more detailed and maintained.
- **EveryInc compound-engineering `ce-code-review` and `ce-test-browser`:** a heavier multi-reviewer plugin that overlaps our own review agents.
- **Community "engineering-manager" skills on skills.sh:** these are about managing people, not reviewing features.
