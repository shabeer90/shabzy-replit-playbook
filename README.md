# shabzy-replit-playbook

A starter kit for a new project built on Replit with coding agents: Replit Agent and Claude Code. It holds the rules, agents, hooks, CI and repo layout that worked on earlier projects, and the lessons that came out of them.

**To start a new project:** copy `template/` into the new repo, then give the agent the prompt in [STARTER-PROMPT.md](STARTER-PROMPT.md).

| File | What it is |
|---|---|
| [STARTER-PROMPT.md](STARTER-PROMPT.md) | The first message to give an agent in a new project |
| [PLAYBOOK.md](PLAYBOOK.md) | The rules and checklists, each with the project it came from |
| [SKILLS.md](SKILLS.md) | The skills we use, what each is for, and how to install them |
| [template/](template/) | Files to copy into a new repo: agent rules, agents, hooks, CI, design-system check |
| [learnings/](learnings/) | One file per project: what happened, raw, before it becomes a rule |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How a project adds what it learned |

## How the pieces fit

```
AGENTS.md            ← one set of rules for every agent (Claude Code, Replit Agent, others)
  ├─ CLAUDE.md       ← Claude Code reads this; it imports AGENTS.md
  └─ replit.md       ← Replit Agent reads this; it points to AGENTS.md
.claude/agents/      ← owners: head-of-design, head-of-data. Reviewers: em, qa, cto, security, seo-geo
.claude/reviewers.txt ← which reviewers must sign off on this project
.claude/hooks/       ← guard.py: blocks secrets, pushes to main, dangerous scripts, and PRs until every listed reviewer signs off
.github/workflows/   ← pr-checks.yml: types, tests, design-system check, build, e2e
scripts/check_design_system.py ← pages may only use design tokens and shared components
```

## Sources

- **Cogniscore** (cogniscore.co.uk, May to Nov 2026): the first project. See [learnings/cogniscore.md](learnings/cogniscore.md).
