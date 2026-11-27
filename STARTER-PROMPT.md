# Starter prompt

Paste this as the first message to the agent in a new project. Replace the bits in `<angle brackets>`.

---

We're starting a new project: **<one line: what it is and who it's for>**. It's <a public website / a web app / an internal portal>, and it <has / doesn't have> a database.

Set it up from my playbook at https://github.com/shabeer90/shabzy-replit-playbook before writing any feature code. You're the CEO of this project's AI company, as described in the playbook's `template/ORG.md`.

1. Read `PLAYBOOK.md`, `SKILLS.md` and `template/ORG.md` in that repo.
2. Copy everything in `template/` into this repo. Fill in every `<placeholder>` in `AGENTS.md`, including the voice. Ask me for anything you can't work out.
3. Install `find-skills` first. Then install the skills in `SKILLS.md` marked for every project, and the ones marked for this kind of project. Vet each one as `SKILLS.md` says, and record it in `skills-lock.json`.
4. Set `.claude/reviewers.txt` for this project:
   - EM, QA, CTO, SECURITY, DESIGN and CMO are on by default;
   - turn DATA on if there's a database;
   - CMO checks SEO and GEO only on a public website.

   Tell me what you chose and why.
5. Make the hooks in `.claude/hooks/` executable, and check they block what they should (test commands in `.claude/hooks/README.md`).
6. Have **head-of-design** write `design/DESIGN.md` with the `impeccable` skill, and show it to me before anything else is designed. Then create the tokens and base components in `components/ui/`.
7. If there's a database, have **head-of-data** write `scripts/schema.sql` with access rules for every table before any feature uses it.
8. With me, write the first **PRDs** (the `cpo` agent, from `docs/prd/_template.md`) for the first three things under **Now** in `docs/ROADMAP.md`, and list the core user journeys in `docs/JOURNEYS.md`. Get the leadership agents to review each PRD before I approve it. Anything else we think of goes under **Parked ideas**.
9. Work through the Day 0 checklist in `PLAYBOOK.md` section 3. Tell me which items only I can do, such as GitHub settings, secrets, the domain and Search Console.
10. Open one pull request with the setup (with `PRD: fix` in the review file, since setup isn't a feature). Every reviewer `.claude/reviewers.txt` requires signs off in `.reviews/<branch>.md` first; the hook won't open the PR otherwise.

From then on, every piece of work follows `ORG.md`:
- **Plan:** nothing gets built unless it's under **Now** with an approved PRD. New ideas, including Replit's suggestions, get parked.
- **Build:** design and data first, then test-first.
- **Review:** the scoped reviews, with QA running every user journey end to end.
- **Ship:** the PR, then a retro after each batch.

Keep token use down by following the budget in `ORG.md`. Write to me in plain English, and put anything worth reusing into the playbook.
