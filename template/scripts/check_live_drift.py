#!/usr/bin/env python3
"""Scheduled check: the live site runs a commit that's on main, with nothing uncommitted (PLAYBOOK rule 1).

Replit publishes whatever is in the workspace. Branch protection stops unreviewed code reaching main,
but not reaching the live site. This reads the commit the site reports (scripts/write_version.sh) and fails when:
  - the site reports nothing, or `unknown`;
  - the build had uncommitted changes (`-dirty`);
  - the commit isn't on main (published from a branch, or from a commit nobody pushed);
  - a merge to main that changes the site has waited more than MAX_HOURS without being published.
    Merges that only touch docs/ or the Markdown files at the root don't count: republishing for them changes nothing.

Usage: SITE_URL=https://example.com python scripts/check_live_drift.py [max_hours, default 24]
"""
import os
import re
import subprocess
import sys
import time
import urllib.request


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def problems(live, main="origin/main", max_hours=24, now=None):
    live = live.strip()
    if not live or live == "unknown":
        return ["the live site doesn't say which commit it runs. Check that the build runs scripts/write_version.sh "
                "and that git is available when Replit builds."]
    sha = live.removesuffix("-dirty")
    if not re.fullmatch(r"[0-9a-f]{7,40}", sha):
        return [f"version.txt doesn't hold a commit: {live[:40]!r}"]
    if live.endswith("-dirty"):
        return [f"the live site was built from {sha[:12]} plus uncommitted workspace changes. "
                "Put them through a PR, then republish from main."]
    if git("cat-file", "-e", f"{sha}^{{commit}}")[0]:
        return [f"the live commit {sha[:12]} isn't on GitHub: it was published from a commit nobody pushed."]
    if git("merge-base", "--is-ancestor", sha, main)[0]:
        return [f"the live commit {sha[:12]} isn't on main: it was published from a branch, before review."]
    # First-parent commits on main are the merges themselves, dated when they landed.
    waiting = [int(t) for t in git("log", "--first-parent", "--format=%ct", f"{sha}..{main}", "--",
                                   ".", ":(exclude)docs", ":(exclude,glob)*.md")[1].split()]
    if waiting:
        hours = ((now or time.time()) - min(waiting)) / 3600
        if hours > max_hours:
            return [f"{len(waiting)} merge(s) to main aren't live, the oldest from {hours:.0f} hours ago. "
                    "Pull main in the Replit Shell and republish."]
    return []


def main():
    url = os.environ["SITE_URL"].rstrip("/") + f"/version.txt?t={int(time.time())}"
    try:
        live = urllib.request.urlopen(url, timeout=20).read(200).decode(errors="replace")
    except Exception as e:  # report it as "no commit" below, never pass silently
        print(f"Couldn't fetch {url}: {e}")
        live = ""
    found = problems(live, max_hours=float(sys.argv[1]) if len(sys.argv) > 1 else 24)
    for p in found:
        print(f"Live drift: {p}")
    if found:
        sys.exit(1)
    print(f"Live drift: ok, the site runs {live.strip()[:12]} from main.")


if __name__ == "__main__":
    main()
