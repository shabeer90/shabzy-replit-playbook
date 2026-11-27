# Skills

Install with the [Skills CLI](https://skills.sh), which records each skill in `skills-lock.json`:

```bash
npx skills add <github-owner/repo> --skill <name>
```

Every installed skill must be in `skills-lock.json`. On Cogniscore, 7 of 15 were missing, so nobody could tell where they came from or whether they had changed.

## Every project

| Skill | Source | Use it for |
|---|---|---|
| ponytail | local copy; record the source when installing | All coding: the smallest change that fully solves the task |
| frontend-design | anthropics/skills | Building UI that doesn't look generic |
| web-design-guidelines | vercel-labs/agent-skills | Reviewing UI against interface guidelines and accessibility |
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill | Palettes, type pairings, UX rules; used by head-of-design |
| skill-creator | anthropics/skills | Writing project skills (for example the project's own Reddit or release skill) |
| codebase-design | mattpocock/skills | Module and interface design; used by cto-reviewer |

## Review and QA (every project)

These back the EM and QA agents. All were checked to exist in their repos on 27 Nov 2026. Read each SKILL.md before installing.

| Skill | Source | Used by | Use it for |
|---|---|---|---|
| webapp-testing | anthropics/skills | qa-tester | Drives the local app with Playwright: checks features, screenshots, browser logs |
| code-review | mattpocock/skills | em-reviewer | Reviews a diff against the spec and the repo's standards, in parallel sub-agents |
| to-spec | mattpocock/skills | the builder, before starting | Turns the conversation into a written spec the EM checks against |
| tdd | mattpocock/skills | the builder | Red-green-refactor, so features arrive with tests |
| diagnosing-bugs | mattpocock/skills | anyone | A diagnosis loop for hard bugs, before guessing at a fix |

Also looked at, not chosen:
- **EveryInc compound-engineering `ce-code-review` / `ce-test-browser`:** a heavier multi-reviewer setup, and a plugin rather than a single skill.
- **Community "engineering-manager" skills on skills.sh:** these are about people management, not feature review.

Our own `em-reviewer` agent does the EM job instead.

## When the project needs it

| Skill | Source | When |
|---|---|---|
| next-best-practices | vercel-labs/next-skills | Next.js projects |
| supabase-postgres-best-practices | supabase/agent-skills | Projects with Postgres or Supabase; used by head-of-data: schema, RLS, migrations |
| seo-audit | coreyhaines31/marketingskills | Public sites; used by seo-geo-reviewer: ranking and indexing |
| seo-geo | resciencelab/opc-skills | Public sites; used by seo-geo-reviewer: schema markup, AI-search visibility |
| audit-website | squirrelscan/skills | A full site crawl before launch and monthly after |
| security-audit | cloudflare/security-audit-skill | Recommended by security-reviewer before launch and after big changes. Run on a read-only copy, outside the repo, with no network. Expensive: choose the depth first. |
| improve-codebase-architecture | mattpocock/skills | When the code has grown and needs restructuring |

## Built into Claude Code (no install)

- `/code-review`: review the current diff for bugs. The cto-reviewer agent uses it.
- `/security-review`: a security pass on the branch.
- `/simplify`: cleanup without hunting bugs.

## Project skills

Write one with skill-creator when the project repeats a workflow with house rules. On Cogniscore these were Reddit replies drafted for manual posting, and releasing a brand's evidence.
