# Skills

Install with the [Skills CLI](https://skills.sh), which records each skill in `skills-lock.json`:

```bash
npx skills add <github-owner/repo> --skill <name>
```

Every installed skill must be in `skills-lock.json`. On Cogniscore, 7 of 15 were missing, so nobody could tell where they came from or whether they had changed.

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

## Every project

| Skill | Source | Use it for |
|---|---|---|
| find-skills | vercel-labs/skills | Finding an existing skill before doing a new kind of task (see above) |
| ponytail | local copy; record the source when installing | All coding: the smallest change that fully solves the task |
| frontend-design | anthropics/skills | Building UI that doesn't look generic |
| web-design-guidelines | vercel-labs/agent-skills | Reviewing UI against interface guidelines and accessibility |
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill | Palettes, type pairings, UX rules; used by head-of-design |
| skill-creator | anthropics/skills | Writing project skills (for example the project's own Reddit or release skill) |
| codebase-design | local copy; source not recorded | Module and interface design; used by cto-reviewer |

## When the project needs it

| Skill | Source | When |
|---|---|---|
| next-best-practices | vercel-labs/next-skills | Next.js projects |
| supabase-postgres-best-practices | supabase/agent-skills | Any Supabase or Postgres work: schema, RLS, migrations |
| seo-audit | coreyhaines31/marketingskills | Public sites: diagnosing ranking and indexing |
| seo-geo | resciencelab/opc-skills | Public sites: schema markup, AI-search visibility |
| audit-website | squirrelscan/skills | A full site crawl before launch and monthly after |
| security-audit | cloudflare/security-audit-skill | Before launch and after big changes. Run on a read-only copy, outside the repo, with no network. Expensive: choose the depth first. |
| improve-codebase-architecture | local copy; source not recorded | When the code has grown and needs restructuring |

## Working style (mattpocock/skills)

| Skill | Use it for |
|---|---|
| grilling | Stress-testing a plan before building it |
| research | Investigating a question against primary sources and saving the findings in the repo |
| retro | A retrospective after a batch or a hard session |
| writing-for-agents | Writing skills, AGENTS.md and CLAUDE.md that agents follow |
| teach | Learning a new area with a structured plan |

## Built into Claude Code (no install)

- `/code-review`: review the current diff for bugs. The cto-reviewer agent uses it.
- `/security-review`: a security pass on the branch.
- `/simplify`: cleanup without hunting bugs.

## Project skills

Write one with skill-creator when the project repeats a workflow with house rules. On Cogniscore these were Reddit replies drafted for manual posting, and releasing a brand's evidence.
