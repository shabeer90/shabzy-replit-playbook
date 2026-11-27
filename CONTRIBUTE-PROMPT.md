# Contribute prompt

Paste this into a project to add what it has learned to the playbook. To set up a new project, use [STARTER-PROMPT.md](STARTER-PROMPT.md). To bring an existing one up to date, use [UPGRADE-PROMPT.md](UPGRADE-PROMPT.md).

---

I keep a shared playbook for all my projects at https://github.com/shabeer90/shabzy-replit-playbook. Add this project's lessons to it, so the next project benefits.

1. Read the playbook first: README.md, CONTRIBUTING.md, PLAYBOOK.md (especially the numbered rules), template/ORG.md, SKILLS.md, learnings/_template.md, and any existing learnings/<this-project>.md. CONTRIBUTING.md says where each kind of change goes. Follow it exactly.

2. Go through this project and list what it learned. Look at:
   - git history and PR descriptions;
   - retros and docs;
   - agent memory (replit.md, .agents/memory/, AGENTS.md, CLAUDE.md);
   - tests whose comments explain a past bug;
   - CI workflows.

   Look for anything that broke, cost time or money, or worked unusually well. Especially:
   - Replit platform quirks;
   - security or data mistakes;
   - deploys that didn't go live;
   - feature creep;
   - broken user journeys;
   - token or cost surprises;
   - skills or agents that helped.

3. Apply [the contribution bar](CONTRIBUTING.md#the-bar-for-a-rule), then check each lesson against the playbook:
   - **Already covered:** skip it. If this project adds a useful example, add one "*On <project>:*" line under that rule instead.
   - **Covered but wrong for this project:** propose rewriting the rule in place, with one line saying what changed.
   - **Not covered:** propose where it goes, per CONTRIBUTING.md.

   Never renumber rules. Never add a second version of something that already exists.

4. Show me the list before changing anything: each lesson, where it would go, and the evidence from this project (file, commit or PR). I'll pick which ones go in.

5. For the ones I approve:
   - add each one to learnings/<this-project>.md using the exact format in learnings/_template.md (create the file from the template if it doesn't exist), numbered after the last existing lesson;
   - add or update rules, checklists, agent files or SKILLS.md only where CONTRIBUTING.md says to;
   - add a line to CHANGELOG.md under the next version (patch, minor or major, per CONTRIBUTING.md's Versions section).

6. Write the way the playbook is written: plain English, short sentences, specific, nothing that sounds AI-written. A new rule says what to do. Its "*On <this project>:*" line goes in PLAYBOOK.md, never in agent files, ORG.md or SKILLS.md.

7. The playbook repo is public:
   - no secrets, keys, database IDs, customer data or personal details;
   - a security issue that isn't fixed yet in this project goes in as "Held back": title, kind and home only.

8. Clone the playbook repo, make the changes on a new branch, and open a pull request. Don't push to main. If you can't open a PR from here, put the changed files in a folder in this project and tell me, and I'll open the PR from Claude Code.

Tell me plainly what you found, what you're proposing, and what you skipped.
