# Starter prompt

Paste this as the first message to the agent in a new project. Replace the bits in `<angle brackets>`.

---

We're starting a new project: **<one line: what it is and who it's for>**. It's <a public website / a web app / an internal portal>, and it <has / doesn't have> a database. Run it <lite / full> (`template/ORG.md`, "Lite or full"); on lite, skip the steps and agents that section leaves out.

Set it up from my playbook at https://github.com/shabeer90/shabzy-replit-playbook before writing any feature code. You're the CEO of this project's AI company, as described in the playbook's `template/ORG.md`. The hooks, review agents and skills only bind Claude Code (PLAYBOOK, "How the company works"). If you're Replit Agent, follow `template/replit.md` by hand, since the hooks won't stop you, and tell me which steps need Claude Code (the hook tests in step 6 and the reviews in step 12).

1. Check that the PLAYBOOK Day 0 list is done: the repo on GitHub with `main` protected, imported into Replit, secret scanning on, and a non-production database if there's a database. List what's missing and wait until I've done it.
2. Read `PLAYBOOK.md`, `SKILLS.md` and `template/ORG.md` in that repo, and the modules in `modules/` that fit this project (`PLAYBOOK.md` lists them).
3. Copy everything in `template/` into this repo. Fill in every `<placeholder>` in every copied file, including the voice in `AGENTS.md` and the pinned versions in `pr-checks.yml`. Adapt CI to this stack. Ask me for anything you can't work out.
4. Install `find-skills` first. Then install the skills in `SKILLS.md` under *Every project* and *Product, review and QA*, plus the sections that fit this kind of project. Vet each one as `SKILLS.md` says, and record it in `skills-lock.json`.
5. Set `.claude/reviewers.txt` for this project, with paths that match this repo's real folders:
   - on lite, as `ORG.md` says;
   - on full, EM, QA, CTO, SECURITY, DESIGN and CMO are on by default;
   - turn DATA on if there's a database;
   - CMO checks SEO and GEO only on a public website.

   Tell me what you chose and why.
6. Make the hooks in `.claude/hooks/` executable, and check they block what they should (test commands in `.claude/hooks/README.md`).
7. List every Replit workflow, port, artifact and scaffold (mockup sandbox, `api-server` stub, Canvas). Delete what we won't use once I've agreed, and write the port map to `.agents/memory/`.
8. Make the app build and serve its production output, and point Playwright at that, not the dev server (PLAYBOOK rule 17, and `modules/replit-platform.md` for Playwright on Replit). Fill in `playwright.config.ts`, `config/bundle.json` and the provider list in `scripts/check_external_writes.py`, and get `e2e/home.spec.ts` passing against the built output.
9. Have **head-of-design** write `design/DESIGN.md` with the `impeccable` skill, and show it to me before anything else is designed. Then create the tokens and base components in `components/ui/`.
10. If there's a database, have **head-of-data** write `scripts/schema.sql` with access rules for every table before any feature uses it. Decide where uploaded files live (not the published filesystem; `modules/replit-platform.md`).
11. With me, write the first **PRDs** (the `cpo` agent, from `docs/prd/_template.md`) for the first three things under **Now** in `docs/ROADMAP.md`, and list the core user journeys in `docs/JOURNEYS.md`. Get the leadership agents to review each PRD before I approve it. Anything else we think of goes under **Parked ideas**.
12. Open one pull request with the setup (with `PRD: fix` in the review file, since setup isn't a feature). Every reviewer that `.claude/reviewers.txt` requires signs off in `.reviews/<branch>.md` first; the hook won't open the PR otherwise.

Setup is done when the hook tests give the expected exit codes, CI is green on the setup PR, and the journey test passes against the built app. Then go through the PLAYBOOK first-week checklist and mark each item done, mine, or not yet.

From then on, follow `ORG.md`: nothing gets built without an approved PRD under **Now**, and new ideas, including Replit's suggestions, get parked. Report the agents run and rough token use in each retro. Write to me in plain English, and put anything worth reusing into the playbook.
