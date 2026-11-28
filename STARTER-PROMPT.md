# Starter prompt

Paste this as the first message to the agent in a new project. Replace the bits in `<angle brackets>`.

---

We're starting a new project: **<one line: what it is and who it's for>**. It's <a public website / a web app / an internal portal>, and it <has / doesn't have> a database. Its stage is <exploring / launched> (`template/ORG.md`, "Stages"); a brand-new idea is exploring.

Set it up from my playbook at https://github.com/shabeer90/shabzy-replit-playbook before writing any feature code. You're the CEO of this project's AI company (`template/ORG.md`). You may be Replit Agent or Claude Code: the setup is the same, and the steps only Claude Code can do are marked.

1. Check that the PLAYBOOK Day 0 list is done: the repo on GitHub with `main` protected (GitHub Pro if it's private), imported into Replit, and a non-production database if there's a database. List what's missing and wait until I've done it.
2. Read `PLAYBOOK.md` and `template/ORG.md` in that repo, and the modules in `modules/` that fit this project. This is the one time you read it all.
3. Copy everything in `template/` into this repo, keeping `.claude/skills` as a link to `.agents/skills`. Fill in every `<placeholder>`, including the stage and voice in `AGENTS.md` and the pinned versions in the workflows. Adapt CI to this stack. Ask me for anything you can't work out.
4. Set `config/lanes.json` and `.agents/skills/review/lenses.txt` to this repo's real folders. Turn the DATA lens on if there's a database; the WORDS lens checks SEO and GEO only on a public website. Tell me what you chose.
5. Install `find-skills` first. Then install the skills in `SKILLS.md` under *Every project*, plus the sections that fit this kind of project. Vet each one as `SKILLS.md` says, and record it in `skills-lock.json`.
6. Make the app build and serve its production output, and point Playwright at that, not the dev server (PLAYBOOK rule 17, and `modules/replit-platform.md` for Playwright on Replit). Make the build run `scripts/write_version.sh`. Fill in `playwright.config.ts`, `config/bundle.json` and the provider list in `scripts/check_external_writes.py`, and get `e2e/home.spec.ts` passing against the built output.
7. List every Replit workflow, port, artifact and scaffold (mockup sandbox, `api-server` stub, Canvas). Delete what we won't use once I've agreed, and write the port map to `.agents/memory/`.
8. If there's a database, have **head-of-data** write `scripts/schema.sql` with access rules for every table before any feature uses it. Decide where uploaded files live (not the published filesystem; `modules/replit-platform.md`).
9. With me, put the first one to three items under **Now** in `docs/ROADMAP.md`, each with its lane, and write a PRD for each Feature or Bet (`docs/prd/_template.md`). Anything else we think of goes under **Parked ideas**.
10. Write `docs/prd/<date>-setup.md`, a short PRD whose **Undo** is reverting the PR, and get my approval. The setup is a Bet: it adds CI and the hooks.
11. **Claude Code only:** make the hooks in `.claude/hooks/` executable and check they block what they should (`.claude/hooks/README.md`). Then run the `reviewer` agent on the setup PRD in PRD mode, and on the branch, and `qa-tester` on the branch.
12. Open one pull request with the setup. Its description starts with `Lane: bet`, `Door: one-way (it adds CI and hooks)`, a blast radius, and `PRD: docs/prd/<date>-setup.md`. If you're Replit Agent, open it as `template/replit.md` says, and I'll have Claude Code review it or read it myself.

Setup is done when CI is green on the setup PR (the lane check starts with the next PR, because it runs from `main`) and the journey test passes against the built app. If the stage is launched, go through the PLAYBOOK before-launch list and mark each item done, mine, or not yet. If it's exploring, stop there.

From then on, start every change with the `lane` skill: nothing becomes a Feature or Bet without an approved PRD under **Now**, and new ideas, including your own suggestions, get parked. Write to me in plain English, and put anything worth reusing into the playbook.
