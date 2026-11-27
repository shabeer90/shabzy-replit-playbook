#!/usr/bin/env python3
"""Public pages load little JavaScript and never pull in private code (PLAYBOOK section 7).

Run after the build. Reads config/bundle.json, then walks the static imports of each public entry
in Vite's manifest. Fails if a reached chunk comes from a private source, or the entry's JavaScript
is over budget. Dynamic imports aren't followed: they load later, and private APIs still need auth.
Not a Vite project? Replace this step in pr-checks.yml with your framework's equivalent.
"""
import json
import pathlib
import sys


def problems(config_path="config/bundle.json"):
    cfg_file = pathlib.Path(config_path)
    if not cfg_file.exists():
        return [f"{config_path} is missing: set the manifest, public entries, private sources and budget"]
    cfg = json.loads(cfg_file.read_text())
    manifest_path = pathlib.Path(cfg["manifest"])
    if not manifest_path.exists():
        return [f"{manifest_path} not found: run the build first (Vite needs build.manifest: true)"]
    manifest = json.loads(manifest_path.read_text())
    out_dir = manifest_path.parent.parent if manifest_path.parent.name == ".vite" else manifest_path.parent
    found = []
    for entry in cfg["publicEntries"]:
        if entry not in manifest:
            found.append(f"public entry {entry} is not in the manifest")
            continue
        seen, stack = set(), [entry]
        while stack:
            key = stack.pop()
            if key in seen:
                continue
            seen.add(key)
            stack.extend(manifest[key].get("imports", []))
        for key in sorted(seen):
            src = manifest[key].get("src", key)
            if any(src.startswith(p) for p in cfg["privateSources"]):
                found.append(f"{entry} statically imports private code: {src}")
        size = sum((out_dir / manifest[k]["file"]).stat().st_size
                   for k in seen if manifest[k]["file"].endswith(".js"))
        if size > cfg["budgetKiB"] * 1024:
            found.append(f"{entry} loads {size / 1024:.0f} KiB of JavaScript; the budget is {cfg['budgetKiB']} KiB")
    return found


if __name__ == "__main__":
    found = problems()
    print("\n".join(found) or "bundle within budget, no private code in public entries")
    sys.exit(1 if found else 0)
