@AGENTS.md

## Claude Code specifics

- Use the `ponytail` skill for all coding.
- When a feature is built, run every reviewer listed in `.claude/reviewers.txt` as subagents, in parallel. Fix what they confirm, and re-run any that said "fix first". `gh pr create` is blocked until `.reviews/<branch>.md` has all of them at `ship`.
- Schema or data changes go through `head-of-data` before they're built.
- Any UI change goes through `head-of-design` when it needs a component or token that doesn't exist yet.
- Right after opening a PR, turn on Auto-fix (the CI monitor) for it. Don't poll CI yourself.
