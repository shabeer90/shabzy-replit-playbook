# shabzy-replit-playbook

This is how I start and run my projects. I build them on Replit with Claude Code and Replit Agent. Each project is run like a small company where the agents do the work and I make the decisions.

Most of what's here I learned the hard way, first on Cogniscore, then on Ihsan and Impact Connect. This repo exists so the next project doesn't repeat those mistakes. When a project teaches me something new, it goes back in here, with the evidence for what worked, what failed and what to do differently next time. The test is whether the same mistakes stop coming back.

## Starting a new project

Open a new Replit project and paste [STARTER-PROMPT.md](STARTER-PROMPT.md) as your first message to the agent. The agent copies the `template/` folder into the project and walks you through setup. It asks you for the things only you can do, like GitHub settings, secrets and the domain.

## Upgrading an existing project

When the playbook changes, paste [UPGRADE-PROMPT.md](UPGRADE-PROMPT.md) into the project. The agent checks what's new since the project's version, shows you the gaps, and opens a PR with the ones you approve.

## Adding what a project learned

Paste [CONTRIBUTE-PROMPT.md](CONTRIBUTE-PROMPT.md) into the project. The agent finds what's new, checks it against what's already here, shows you the list, and opens a PR with the lessons you approve.

## What's in here

- **[PLAYBOOK.md](PLAYBOOK.md):** the rules. Most say which project they came from and what went wrong, so you can decide whether they apply to yours. The rest are how I've chosen to work. It also has the setup checklists.
- **[template/ORG.md](template/ORG.md):** who does what. There's a CEO, CPO, CTO and CMO, each with their own agents, and I'm the board. It also covers how a piece of work goes from idea to live, and how to keep token use down.
- **[SKILLS.md](SKILLS.md):** the skills the agents use, what each one is for, and how to check a new one before installing it.
- **[template/](template/):** the files every project starts with: agent instructions, the review agents, a hook that blocks risky actions, CI, and starter files for design and product planning.
- **[learnings/](learnings/):** one file per project, all in the same format ([`_template.md`](learnings/_template.md)).
- **[CONTRIBUTING.md](CONTRIBUTING.md):** where each kind of change goes, so the playbook doesn't end up saying the same thing twice in different words.
- **[CHANGELOG.md](CHANGELOG.md):** what changed, and when.

## Two rules that matter most

**Nothing gets built without a PRD.** Replit is quick to suggest new features, and it's tempting to build them all. My projects drifted that way. Now every idea goes on a parked list in `docs/ROADMAP.md`, and only work with an approved PRD gets built.

**The user's journey has to work end to end.** A new feature that works on its own but breaks the path a user takes through the product isn't finished. The QA and engineering-manager agents check every journey on every change.

## The template, file by file

```
template/
  AGENTS.md                instructions every agent follows
    CLAUDE.md              Claude Code reads this; it pulls in AGENTS.md
    replit.md              Replit Agent reads this; it points to AGENTS.md
  ORG.md                   who owns what
  .gitignore               keeps secrets, builds and review notes out of git
  GLOSSARY.md              the project's words, defined once
  .claude/agents/          the product, design and data leads, and the reviewers
  .claude/reviewers.txt    which reviewers this project needs
  .claude/settings.json    turns the guard hook on for Claude Code
  .claude/hooks/           the guard (stops secrets, pushes to main, and PRs nobody has reviewed),
                           its blocked-commands list, and how to test it
  .agents/memory/          facts agents shouldn't have to relearn
  .github/workflows/       the checks every pull request has to pass
  design/                  the design direction and design tokens
  components/ui/           the shared components every page is built from
  docs/prd/                one PRD per piece of work
  docs/ROADMAP.md          what we're building now, and the parked ideas
  docs/JOURNEYS.md         the user journeys that must always work
  docs/retro-template.md   the retro written after each batch
  lib/json-ld.ts           structured data that can't break out of its script tag
  scripts/                 the design-system check, a URL safety check, and the
                           check that new tests fail before the fix
```

## Projects so far

- **Cogniscore** ([cogniscore.co.uk](https://cogniscore.co.uk)), May to November 2026: [learnings/cogniscore.md](learnings/cogniscore.md).
- **Ihsan**, November 2026: [learnings/ihsan.md](learnings/ihsan.md).
- **Impact Connect**, August to November 2026: [learnings/impact-connect.md](learnings/impact-connect.md).
