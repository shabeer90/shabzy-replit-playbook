# Hooks

`guard.py` runs before every Bash, Write and Edit call that Claude Code makes in this repo (wired up in `.claude/settings.json`). It blocks:

- secrets written into tracked files;
- commits that contain secrets, and `--no-verify`;
- pushes to `main` and force pushes;
- anything listed in `blocked-commands.txt`;
- `gh pr create` until `.reviews/<branch>.md` has `<NAME>: ship` for every reviewer in `.claude/reviewers.txt`.

Hooks bind Claude Code only. Replit Agent and humans are covered by GitHub push protection, secret scanning and branch protection, so turn those on too.

## Check it works

Run from the repo root:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git push origin main"}}' | python3 .claude/hooks/guard.py; echo "exit $?"
```

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":".replit","content":"KEY=ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}' | python3 .claude/hooks/guard.py; echo "exit $?"
```

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git push -u origin my-branch"}}' | python3 .claude/hooks/guard.py; echo "exit $?"
```

The first two should print a reason and exit 2. The third should exit 0.
