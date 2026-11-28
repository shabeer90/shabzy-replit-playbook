# Hooks

`guard.py` runs before every Bash, Write, Edit and MultiEdit call that Claude Code makes in this repo (wired up in `.claude/settings.json`). It blocks:

- secrets written into any file except a `.env*` file (other than `.env.example`);
- commits that contain secrets, and `--no-verify`;
- pushes to `main` and force pushes;
- anything listed in `blocked-commands.txt`;
- `gh pr create` until `.reviews/<branch>.md` (`/` in the branch name becomes `-`) has a `Lane:` line and, for a Feature or Bet, `REVIEW: ship`, plus `QA: ship` when the branch touches QA's paths in `.agents/skills/review/lenses.txt`. A Fix opens without reviews.

Hooks bind Claude Code only. Everything else rests on GitHub: branch protection with the `pr-checks`, `pr-e2e` and `pr-lane` checks required, and secret scanning (PLAYBOOK, "What enforces each rule"). The lane and PRD are checked there, in CI, for every author, so the hook doesn't repeat them.

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

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"gh pr create --title t --body b"}}' | python3 .claude/hooks/guard.py; echo "exit $?"
```

Run these on a branch, not `main`. The first two and the last should print a reason and exit 2 (the last because `.reviews/<branch>.md` has no `Lane:` line yet). The third should exit 0.
