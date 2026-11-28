@AGENTS.md

## Claude Code specifics

- Use the `ponytail` skill for all coding.
- The project skills in `.agents/skills/` reach you through the `.claude/skills` link **(check current docs)**. If `lane`, `review` or `release` isn't listed as a skill, read its `SKILL.md` directly.
- Start every change with the `lane` skill, and write its four header lines at the top of `.reviews/<branch>.md`.
  - **Fix:** build it, run CI's checks, open the PR. No review agents.
  - **Feature:** an approved PRD under **Now** first (the `cpo` agent writes it). `head-of-design` or `head-of-data` go first if it needs something new from them. Then the `reviewer` agent, and `qa-tester` if it touches the app, as subagents in parallel.
  - **Bet:** as a Feature, and the `reviewer` agent reviews the PRD before the owner approves it.
- `gh pr create` is blocked until `.reviews/<branch>.md` has a `Lane:` line and, for a Feature or Bet, `REVIEW: ship` (and `QA: ship` when QA's paths are touched). Paste the file into the PR description, since CI reads the header there.
- On a PR that Replit Agent opened, run the `reviewer` (and `qa-tester`) on its branch and paste the review into the PR as a comment.
- Right after opening a PR, turn on Auto-fix (the CI monitor) for it. Don't poll CI yourself.
- Before a new kind of task, check for an existing skill with `find-skills` (vetting rules in the playbook's SKILLS.md).
