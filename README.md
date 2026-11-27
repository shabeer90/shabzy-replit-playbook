# shabzy-replit-playbook

How we start and run every project: as a small AI company. Agents hold the jobs, the owner is the board, and each project leaves the next one a little better and more autonomous.

Projects so far have been built on Replit with Claude Code and Replit Agent. Most of this applies to any stack.

**To start a new project:** paste [STARTER-PROMPT.md](STARTER-PROMPT.md) as the agent's first message. It copies `template/` into the repo and sets everything up.

| File | What it is | Change it when |
|---|---|---|
| [STARTER-PROMPT.md](STARTER-PROMPT.md) | The first message to an agent in a new project | The setup steps change |
| [PLAYBOOK.md](PLAYBOOK.md) | The numbered rules, with the project each came from, plus checklists and baselines | A project teaches something the next one should do differently |
| [template/ORG.md](template/ORG.md) | The AI company: roles, feature flow, token budget, autonomy ladder | A role, the flow or the budget changes |
| [SKILLS.md](SKILLS.md) | One skill per job, who uses it, and how to find and vet new ones | A skill is added, replaced or dropped |
| [template/](template/) | Files a project copies: agent rules, agents, hooks, CI, design and data starters | A rule gets enforced by a file |
| [learnings/](learnings/) | One file per project: what happened, before it becomes a rule | After each retro |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Where each kind of change goes, so nothing overlaps | Rarely |
| [CHANGELOG.md](CHANGELOG.md) | What changed in each version | Every merged change |

## How the pieces fit

```
template/
  AGENTS.md              one set of rules for every agent (Claude Code, Replit Agent, others)
    CLAUDE.md            Claude Code reads this; it imports AGENTS.md
    replit.md            Replit Agent reads this; it points to AGENTS.md
  ORG.md                 who owns what: CEO, CPO, CTO, CMO and their teams
  .claude/agents/        cpo, head-of-design, head-of-data, and reviewers: em, qa, cto, security, cmo
  .claude/reviewers.txt  which reviewers this project needs, and which paths wake each one
  .claude/hooks/guard.py blocks secrets, pushes to main, dangerous scripts, and PRs without an approved PRD and reviewer sign-off
  .github/workflows/     pr-checks.yml: types, tests, red-then-green gate, design check, build, e2e
  design/                DESIGN.md (direction) and tokens; components/ui holds the shared components
  docs/prd/              PRDs: no PRD, no feature
  docs/ROADMAP.md        the only list of what gets built; every other idea is parked
  docs/JOURNEYS.md       the user journeys that must always work end to end
```

## Sources

- **Cogniscore** (cogniscore.co.uk, May to Nov 2026): the first project. See [learnings/cogniscore.md](learnings/cogniscore.md).
