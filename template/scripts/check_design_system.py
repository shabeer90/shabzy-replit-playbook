#!/usr/bin/env python3
"""Pages and features may only use design tokens and components/ui. Run in CI and by head-of-design.

Fails on, outside components/ui/ and design/:
  - raw colours: 6/8-digit hex, rgb(), hsl();
  - Tailwind arbitrary values for colour, spacing, size, radius or shadow, such as bg-[#123456] or p-[13px].
A line can opt out with the comment `design-system: allow` plus a reason; the reviewer checks the reason.
"""
import pathlib
import re
import sys

ROOTS = ["app", "src", "components", "pages"]
SKIP = ("components/ui/", "design/")
EXTS = {".tsx", ".jsx", ".ts", ".js", ".css", ".scss", ".vue", ".svelte"}
RAW = re.compile(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?\b|\brgba?\(|\bhsla?\(")
ARBITRARY = re.compile(
    r"\b(?:bg|text|border|fill|stroke|ring|outline|from|via|to|shadow|rounded|"
    r"p[xytrbl]?|m[xytrbl]?|gap|space-[xy]|w|h|min-w|min-h|max-w|max-h|top|left|right|bottom|inset|leading|tracking)-\[")


def problems(root="."):
    base = pathlib.Path(root)
    for top in ROOTS:
        for path in sorted((base / top).rglob("*")):
            rel = path.relative_to(base).as_posix()
            if path.suffix not in EXTS or not path.is_file() or rel.startswith(SKIP) or "node_modules" in rel:
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if "design-system: allow" in line:
                    continue
                if RAW.search(line) or ARBITRARY.search(line):
                    yield f"{rel}:{n}: {line.strip()[:120]}"


if __name__ == "__main__":
    found = list(problems(sys.argv[1] if len(sys.argv) > 1 else "."))
    for p in found:
        print(p)
    if found:
        print(f"\n{len(found)} use(s) of raw values outside the design system. Use a token or a components/ui "
              "component; ask head-of-design to add one if it's missing.")
        sys.exit(1)
    print("Design system check passed.")
