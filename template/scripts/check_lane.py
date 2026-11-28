#!/usr/bin/env python3
"""CI check: the PR says which lane it's in, and the lane fits what it changes (PLAYBOOK rule 31).

The PR description carries four lines (bold markers are fine):
  Lane: fix | feature | bet
  Door: two-way | one-way
  Blast radius: <who or what breaks if this is wrong>
  PRD: fix | docs/prd/<file>.md

Signals only ever raise the lane. A changed file in `one_way_paths` (config/lanes.json) makes the PR a
Bet whatever it says, and a Fix over `fix_max_lines` must become a Feature. This runs in CI, so it binds
Replit Agent and people too; the guard hook binds Claude Code only.

Usage: PR_BODY="<description>" python scripts/check_lane.py origin/main
"""
import fnmatch
import json
import os
import pathlib
import re
import subprocess
import sys

DOOR_OF = {"fix": "two-way", "feature": "two-way", "bet": "one-way"}


def field(body, name):
    m = re.search(rf"^\s*{name}:\s*(.+?)\s*$", body.replace("*", ""), re.I | re.M)
    return m.group(1) if m else ""


def section(text, title):
    m = re.search(rf"^##\s*{title}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    return re.sub(r"<!--.*?-->", "", m.group(1) if m else "", flags=re.S).strip()


def problems(body, changes, config, root="."):
    """changes: [(path, lines changed)]. Returns what's wrong; an empty list passes."""
    lane, door, prd = field(body, "Lane").lower(), field(body, "Door").lower(), field(body, "PRD")
    door = door.split()[0] if door else ""  # "one-way (sends email)" is fine
    if lane not in DOOR_OF:
        return ["the PR description needs a `Lane: fix`, `Lane: feature` or `Lane: bet` line (PLAYBOOK rule 31)."]
    out = []
    if door not in ("one-way", "two-way"):
        out.append("add a `Door: two-way` or `Door: one-way` line.")
    elif door != DOOR_OF[lane]:
        out.append(f"a {door} door can't be a {lane}: one-way doors are Bets, two-way doors are Fixes or Features.")
    if not field(body, "Blast radius"):
        out.append("add a `Blast radius:` line: who or what breaks if this is wrong.")
    skip = config.get("not_one_way", [])
    one_way = sorted({p for p, _ in changes
                      if any(fnmatch.fnmatch(p, pat) for pat in config["one_way_paths"])
                      and not any(fnmatch.fnmatch(p, pat) for pat in skip)})
    if one_way and lane != "bet":
        out.append(f"these files make it a one-way door, so it's a Bet: {', '.join(one_way)}. "
                   "If a path is wrongly listed, change config/lanes.json in its own Bet.")
    if lane == "fix":
        ignore = config.get("ignore_for_size", [])
        size = sum(n for p, n in changes if not any(fnmatch.fnmatch(p, pat) for pat in ignore))
        if size > config["fix_max_lines"]:
            out.append(f"{size} lines changed is over the Fix limit of {config['fix_max_lines']}. "
                       "Split it, or make it a Feature with a PRD.")
        if prd.lower() != "fix":
            out.append("a Fix says `PRD: fix`.")
        return out
    path = pathlib.Path(root, prd)
    text = path.read_text(encoding="utf-8") if prd and path.is_file() else ""
    if not re.search(r"^Status:\s*approved\b", text, re.M):
        out.append(f"a {lane.title()} needs `PRD: docs/prd/<file>.md`, linking a PRD with `Status: approved` "
                   f"(got `{prd or 'nothing'}`).")
    elif lane == "bet" and not section(text, "Undo"):
        out.append(f"{prd} is a Bet with an empty `## Undo` section: say how to switch it off, and what can't be undone.")
    return out


def changed(base):
    out = subprocess.run(["git", "diff", "--numstat", "--no-renames", f"{base}...HEAD"],
                         capture_output=True, text=True, check=True).stdout
    rows = []
    for line in out.splitlines():
        added, deleted, path = line.split("\t", 2)
        rows.append((path, 0 if added == "-" else int(added) + int(deleted)))  # "-" is a binary file
    return rows


def main():
    config = json.loads(pathlib.Path("config/lanes.json").read_text(encoding="utf-8"))
    found = problems(os.environ.get("PR_BODY", ""), changed(sys.argv[1]), config)
    for p in found:
        print(f"Lane check: {p}")
    if found:
        sys.exit(1)
    print("Lane check: ok")


if __name__ == "__main__":
    main()
