@AGENTS.md

## Claude Code specifics

- Use the `ponytail` skill for all coding.
- When a feature is built, run `em-reviewer`, `qa-tester` and `cto-reviewer` as subagents (in parallel), fix what they confirm, and re-run any that said "fix first". `gh pr create` is blocked until `.reviews/<branch>.md` has all three at `ship`.
- Any UI change goes through `head-of-design` when it needs a component or token that doesn't exist yet.
- Right after opening a PR, turn on Auto-fix (the CI monitor) for it. Don't poll CI yourself.
