# Upgrade prompt

Paste this into an existing project to bring it up to the latest playbook version. For a brand-new project, use [STARTER-PROMPT.md](STARTER-PROMPT.md) instead.

---

Upgrade this project to the latest version of my playbook: https://github.com/shabeer90/shabzy-replit-playbook

1. Read the playbook's README.md, CHANGELOG.md, PLAYBOOK.md, the modules in modules/ that fit this project, template/ORG.md, SKILLS.md and CONTRIBUTING.md. Check AGENTS.md for which playbook version this project is on; if it doesn't say, assume none. Read every CHANGELOG entry newer than that version, including its upgrade notes.

2. Compare this project with the playbook's template/ folder, file by file. List for me:
   - files missing here (for example ORG.md, .agents/skills/*, .claude/agents/*, .claude/hooks/guard.py, config/lanes.json, the workflows, docs/prd/, docs/ROADMAP.md, docs/JOURNEYS.md);
   - files here that differ from the template, and whether each difference is a deliberate project choice or just out of date;
   - rules and baselines from the newer versions that this project doesn't follow yet.

   Show me that list before changing anything.

3. For the items I approve:
   - add the missing template files, and fill every <placeholder> from this project's real details;
   - merge template changes into existing files without losing this project's own rules (AGENTS.md, replit.md, CLAUDE.md);
   - set config/lanes.json and .agents/skills/review/lenses.txt to this repo's real folders: the DATA lens on if it has a database, and the WORDS lens checks SEO and GEO only on public pages;
   - set the stage in AGENTS.md: launched if real people use it, otherwise exploring;
   - start docs/ROADMAP.md with what's actually being built now, and park everything else;
   - list the core user journeys in docs/JOURNEYS.md, and say which already have e2e tests;
   - record the playbook version in AGENTS.md.

4. If you're Claude Code, make the hooks executable and run the test commands in .claude/hooks/README.md. Show me which actions were blocked and which were allowed.

5. Work on a branch and open a pull request. If it changes workflows, hooks or config/lanes.json, it's a Bet: write a short PRD for it, with reverting the PR as its Undo, and get my approval. Otherwise it's a Fix or Feature by the `lane` skill. Start the PR description with the skill's four header lines. Don't change app behaviour, auth, rate limits or data as part of this.

6. If something in the playbook is wrong for this project, put it in your report as a suggested playbook change. Don't quietly do it differently.

Tell me plainly what changed, what you skipped and why, and what I need to do (secrets, GitHub settings, approving DESIGN.md or the first PRDs).
