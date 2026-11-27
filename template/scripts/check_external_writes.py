#!/usr/bin/env python3
"""Every call that writes somewhere else has its result checked, not just awaited (PLAYBOOK rule 20).

Fails when a line matching WRITES has no `checked(` (lib/checked.ts) on it or the few lines above.
A line can opt out with the comment `external-write: handled` plus a reason; the reviewer checks it.
Add this project's own providers to WRITES on day one.

Three projects shipped this mistake: a monitor green while sending nothing, a storage helper's
`false` ignored, and an email SDK error ignored while the form said "sent".
"""
import pathlib
import re
import sys

ROOTS = ["app", "src", "server", "lib", "pages", "api", "agents", "jobs"]
EXTS = {".ts", ".tsx", ".js", ".jsx", ".mjs"}
SKIP = ("lib/checked.ts",)
WRITES = re.compile(
    r"\.emails\.send\("                                              # Resend
    r"|\.storage\s*\.from\([^)]*\)\s*\.upload\("                     # Supabase Storage
    r"|\.from\([^)]*\)\s*\.(?:insert|upsert|update|delete)\("        # Supabase / PostgREST
    r"|\.(?:paymentIntents|charges|refunds|transfers)\.create\("    # Stripe
)
LOOKBACK = 3  # shortcut: catches checked( up to 3 lines above; a longer wrapped call needs the opt-out comment


def problems(root="."):
    base = pathlib.Path(root)
    for top in ROOTS:
        for path in sorted((base / top).rglob("*")):
            rel = path.relative_to(base).as_posix()
            if path.suffix not in EXTS or not path.is_file() or rel in SKIP or "node_modules" in rel:
                continue
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for n, line in enumerate(lines, 1):
                if not WRITES.search(line) or "external-write: handled" in line:
                    continue
                if not any("checked(" in l for l in lines[max(0, n - 1 - LOOKBACK):n]):
                    yield f"{rel}:{n}: result not checked: {line.strip()[:100]}"


if __name__ == "__main__":
    found = list(problems())
    print("\n".join(found) or "every external write is checked")
    sys.exit(1 if found else 0)
