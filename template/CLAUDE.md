@AGENTS.md

## Claude Code specifics

- Use the `ponytail` skill for all coding.
- Before handing over a PR, run the `cto-reviewer` agent on the diff and fix what it confirms.
- Any UI change goes through `head-of-design` when it needs a component or token that doesn't exist yet.
- Right after opening a PR, turn on Auto-fix (the CI monitor) for it. Don't poll CI yourself.
