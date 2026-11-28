#!/usr/bin/env python3
"""PreToolUse guard for Claude Code. Exit 2 blocks the tool call and shows the reason to the agent.

Blocks:
  - writing a secret-looking value into any file except a .env* file (.env.example is still checked);
  - `git commit` when the staged diff holds a secret-looking value, and `--no-verify`;
  - `git push` to main/master, and force pushes;
  - any command containing a line from .claude/hooks/blocked-commands.txt (seeders, resets, live writes);
  - `gh pr create` until .reviews/<branch>.md has a `Lane:` line and, for a Feature or Bet, `REVIEW: ship`,
    plus `QA: ship` when the branch touches QA's paths in .agents/skills/review/lenses.txt. A Fix needs no review:
    CI and the owner's read cover it. CI (scripts/check_lane.py) checks the lane and the PRD, for every author.

Why: on an earlier project, provider keys were committed to a config file and stayed in git history.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

SECRET = re.compile(
    r"ghp_[A-Za-z0-9]{36}"
    r"|github_pat_[A-Za-z0-9_]{40,}"
    r"|sk-ant-[A-Za-z0-9_-]{20,}"
    r"|\bre_[A-Za-z0-9]{8}_[A-Za-z0-9]{16,}"   # Resend (format inferred)
    r"|sk_live_[A-Za-z0-9]{20,}"
    r"|sb_secret_[A-Za-z0-9_-]{20,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
)
HERE = os.path.dirname(os.path.abspath(__file__))


def block(reason):
    print(f"Blocked by .claude/hooks/guard.py: {reason}", file=sys.stderr)
    sys.exit(2)


def check_file_write(tool_input):
    path = tool_input.get("file_path", "")
    name = os.path.basename(path)
    if name.startswith(".env") and name != ".env.example":
        return
    texts = [tool_input.get("content", ""), tool_input.get("new_string", "")]
    texts += [e.get("new_string", "") for e in tool_input.get("edits", []) or []]
    if any(SECRET.search(t or "") for t in texts):
        block(f"{path} would contain a secret-looking value. Put it in Replit Secrets, "
              "GitHub secrets or an ignored .env.local, and reference it by name.")


def changed_files():
    """Files this branch changes against main, or None if that can't be worked out (then QA is required)."""
    for base in ("origin/main", "main"):
        out = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"], capture_output=True, text=True)
        if out.returncode == 0:
            return [f for f in out.stdout.splitlines() if f]
    return None


def qa_required():
    """QA signs off when the branch touches QA's paths in lenses.txt, or when the changed files can't be worked out."""
    lenses = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".agents", "skills", "review", "lenses.txt")
    files = changed_files()
    for line in open(lenses, encoding="utf-8") if os.path.exists(lenses) else []:
        parts = line.split("#")[0].split()
        if parts and parts[0] == "QA":
            return files is None or any(fnmatch.fnmatch(f, p) for f in files for p in parts[1:])
    return False


def check_bash(command):
    blocked_file = os.path.join(HERE, "blocked-commands.txt")
    if os.path.exists(blocked_file):
        for line in open(blocked_file, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and line in command:
                block(f"`{line}` is on the project's blocked list (AGENTS.md). The owner runs it.")
    if re.search(r"\bgit\b.*\bpush\b", command):
        tokens = command.split()
        if any(t in ("-f", "--force") or t.startswith("--force-with-lease") or t.startswith("+") for t in tokens):
            block("force push. Ask the owner.")
        targets = {t.split(":")[-1] for t in tokens[tokens.index("push") + 1:] if not t.startswith("-")} if "push" in tokens else set()
        current = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        if "HEAD" in targets:  # `git push origin HEAD` pushes the current branch
            targets = (targets - {"HEAD"}) | {current}
        if targets & {"main", "master"} or (len(targets) <= 1 and current in ("main", "master")):
            block("push to main. Push a branch and open a pull request.")
    if re.search(r"\bgh\s+pr\s+create\b", command):
        branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        review = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".reviews", branch.replace("/", "-") + ".md")
        text = open(review, encoding="utf-8").read() if os.path.exists(review) else ""
        lane = re.search(r"^\**Lane:\**\s*(fix|feature|bet)\b", text, re.M | re.I)
        if not lane:
            block(f"{os.path.relpath(review)} has no `Lane:` line. Use the lane skill (.agents/skills/lane) and put "
                  "its four header lines first. They go into the PR description, where CI checks them.")
        if lane.group(1).lower() != "fix":
            missing = [r for r in ["REVIEW"] + (["QA"] if qa_required() else [])
                       if not re.search(rf"^{r}: ship\s*$", text, re.M)]
            if missing:
                block(f"a {lane.group(1)} needs sign-off from {' and '.join(missing)} in {os.path.relpath(review)}. "
                      "Run the agents it names (reviewer, qa-tester), fix what they find, then open the PR.")
    if re.search(r"\bgit\b.*\bcommit\b", command):
        if "--no-verify" in command:
            block("--no-verify skips the checks.")
        staged = subprocess.run(["git", "diff", "--cached", "-U0"], capture_output=True, text=True).stdout
        added = "\n".join(l for l in staged.splitlines() if l.startswith("+"))
        if SECRET.search(added):
            block("the staged changes contain a secret-looking value. Unstage it and move it to a secret store.")


def main():
    event = json.load(sys.stdin)
    tool, tool_input = event.get("tool_name", ""), event.get("tool_input", {}) or {}
    if tool in ("Write", "Edit", "MultiEdit"):
        check_file_write(tool_input)
    elif tool == "Bash":
        check_bash(tool_input.get("command", ""))


if __name__ == "__main__":
    main()
