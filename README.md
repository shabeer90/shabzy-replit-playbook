# shabzy-replit-playbook

This is how I start and run my projects. I build them on Replit, mostly with Replit Agent, and use Claude Code when it's worth the cost. Each project is run like a small company where the agents do the work and I make the decisions, and how much process a change gets depends on whether it can be undone.

Most of what's here I learned the hard way, on Cogniscore, Impact Connect, Ihsan, Adam Accounting and my personal website. This repo exists so the next project doesn't repeat those mistakes. When a project teaches me something new, it goes back in here, with the evidence for what worked, what failed and what to do differently next time. The test is whether the same mistakes stop coming back.

## Starting a new project

Open a new Replit project and paste [STARTER-PROMPT.md](STARTER-PROMPT.md) as your first message to the agent. The agent copies the `template/` folder into the project and walks you through setup. It asks you for the things only you can do, like GitHub settings and secrets. A new project starts as *exploring*: only the Day 0 list, with the rest of the setup left until there's something to launch.

## Upgrading an existing project

When the playbook changes, paste [UPGRADE-PROMPT.md](UPGRADE-PROMPT.md) into the project. The agent checks what's new since the project's version, shows you the gaps, and opens a PR with the ones you approve.

## Adding what a project learned

Paste [CONTRIBUTE-PROMPT.md](CONTRIBUTE-PROMPT.md) into the project. The agent finds what's new, checks it against what's already here, shows you the list, and opens a PR with the lessons you approve.

## What's in here

- **[PLAYBOOK.md](PLAYBOOK.md):** the rules. Most say which project they came from and what went wrong, so you can decide whether they apply to yours. The rest are how I've chosen to work. It also has the lanes, what enforces each rule, and the setup checklists.
- **[modules/](modules/):** what only some projects need: public sites (SEO, GEO, growth), databases and sign-in, and Replit platform notes. The `lane` skill says when a change needs one.
- **[template/ORG.md](template/ORG.md):** who does what. I'm the board, the main session is the CEO, and specialists wake only when a change needs them. It also covers the stages, the autonomy ladder and how to keep token use down.
- **[SKILLS.md](SKILLS.md):** the skills the agents use, what each one is for, and how to check a new one before installing it.
- **[template/](template/):** the files every project starts with: agent instructions, three project skills (lane, review, release), CI that checks every PR's lane, a daily check that the live site runs `main`, a Claude Code hook that blocks risky actions, and starter files for design and product planning.
- **[learnings/](learnings/):** one file per project, all in the same format ([`_template.md`](learnings/_template.md)).
- **[CONTRIBUTING.md](CONTRIBUTING.md):** where each kind of change goes, so the playbook doesn't end up saying the same thing twice in different words.
- **[CHANGELOG.md](CHANGELOG.md):** what changed, and when.

## Three rules that matter most

**Process follows the door.** A typo fix and a payments change don't get the same process. Anything that can't be undone (money, sent emails, deleted data, sign-in, public claims, URLs) is a Bet and gets the careful path, however small. Everything else moves fast.

**No feature gets built without a PRD.** Replit is quick to suggest new features, and it's tempting to build them all. My projects drifted that way. Now every idea goes on a parked list in `docs/ROADMAP.md`, and nothing bigger than a Fix gets built without an approved PRD.

**The user's journey has to work end to end.** A new feature that works on its own but breaks the path a user takes through the product isn't finished. CI runs every journey's test on every PR, and QA won't sign off a Feature or Bet that broke one.

## The template, file by file

```
template/
  AGENTS.md                instructions every agent follows
    CLAUDE.md              Claude Code reads this; it pulls in AGENTS.md
    replit.md              Replit Agent reads this; it points to AGENTS.md
  ORG.md                   who owns what
  .gitignore               keeps secrets, builds and review notes out of git
  GLOSSARY.md              the project's words, defined once
  .agents/skills/          lane (how much process), review (one reviewer, with lenses by path), release
  .claude/agents/          the product, design and data leads, the reviewer and QA
  .claude/settings.json    turns the guard hook on for Claude Code
  .claude/hooks/           the guard (stops secrets, pushes to main, and Feature or Bet PRs nobody has reviewed),
                           its blocked-commands list, and how to test it
  .agents/memory/          facts agents shouldn't have to relearn
  .github/workflows/       the checks every PR must pass, the lane check, and the daily live-drift check
  design/                  the design direction and design tokens
  components/ui/           the shared components every page is built from
  docs/prd/                one PRD per Feature or Bet
  docs/ROADMAP.md          what we're building now, and the parked ideas
  docs/JOURNEYS.md         the user journeys that must always work
  docs/retro-template.md   the retro written after each batch
  lib/json-ld.ts           structured data that can't break out of its script tag
  lib/checked.ts           turns a failed write (email, storage, payments) into an error
  config/bundle.json       the JavaScript budget and which code is private
  config/lanes.json        the paths that make a PR a Bet, and the Fix size limit
  playwright.config.ts     e2e against the built app, not the dev server
  e2e/                     the first journey test
  scripts/                 the design-system, bundle, external-write, lane and drift checks and
                           their tests, a URL safety check, and the check that new tests fail before the fix
```

## Projects so far

- **Cogniscore** ([cogniscore.co.uk](https://cogniscore.co.uk)), May to November 2026: [learnings/cogniscore.md](learnings/cogniscore.md).
- **Ihsan**, November 2026: [learnings/ihsan.md](learnings/ihsan.md).
- **Impact Connect**, February to November 2026: [learnings/impact-connect.md](learnings/impact-connect.md).
- **Personal Website**, June to November 2026: [learnings/personal-website.md](learnings/personal-website.md).
- **Adam Accounting**, May to November 2026: [learnings/adam-accounting.md](learnings/adam-accounting.md).
