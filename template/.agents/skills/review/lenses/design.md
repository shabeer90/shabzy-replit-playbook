# Design lens

What the user sees. head-of-design owns the design system (`design/DESIGN.md`, `design/tokens/`, `components/ui/`); this lens checks a change against it.

Look at the rendered pages the diff changes, at phone and desktop width. Use `impeccable`'s critique on them. Check for:

- raw colours or arbitrary values outside `components/ui/`;
- a one-off component in a page that duplicates, or should be, a `components/ui/` component;
- missing states: hover, focus, disabled, loading, empty, error;
- accessibility gaps: semantic elements, keyboard reach, visible focus, labels, text contrast of at least 4.5:1;
- anything from head-of-design's list of what makes UI look AI-made (`.claude/agents/head-of-design.md`).

Run `python scripts/check_design_system.py` and include its result.

## In the report

Each issue with file:line, or the page and width, and the fix.
