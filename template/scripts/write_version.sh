#!/usr/bin/env bash
# Writes the commit this build came from to a public file, so the drift check (scripts/check_live_drift.py)
# can compare the live site with main (PLAYBOOK rule 1). Run it first in the build script, for example
#   "build": "scripts/write_version.sh public/version.txt && next build"
# Replit publishes the workspace, not GitHub, so without this nothing tells you the live site is running
# code that never went through a PR. A new file that was never committed isn't flagged; edited tracked files are.
set -u
out="${1:-public/version.txt}"
sha=$(git rev-parse HEAD 2>/dev/null) || sha=unknown
# Tracked changes only: Replit workspaces hold untracked tool folders (.local, .cache, .upm). Lockfiles are left
# out because an install step in the publish build can rewrite them, which would make every build dirty.
if [ "$sha" != unknown ] && [ -n "$(git status --porcelain --untracked-files=no -- . \
    ':!*pnpm-lock.yaml' ':!*package-lock.json' ':!*yarn.lock' 2>/dev/null)" ]; then
  sha="$sha-dirty"
fi
mkdir -p "$(dirname "$out")"
echo "$sha" > "$out"
