@AGENTS.md

## Claude Code specifics

- Use the `ponytail` skill for all coding.
- Follow the feature flow in `ORG.md`:
  - nothing is built without an approved PRD under **Now** in `docs/ROADMAP.md` (the `cpo` agent writes it, and the leadership agents review it);
  - `head-of-design` and `head-of-data` go first when the feature needs something new from them;
  - then every reviewer in `.claude/reviewers.txt` whose paths the change touches runs as a subagent, in parallel.
- `gh pr create` is blocked until `.reviews/<branch>.md` has a `PRD:` line (an approved PRD or `fix`) and every required reviewer at `ship`.
- Right after opening a PR, turn on Auto-fix (the CI monitor) for it. Don't poll CI yourself.
- Before a new kind of task, check for an existing skill with `find-skills` (vetting rules in the playbook's SKILLS.md).
