# Design tokens

`tokens.json` is the single source for colour, fonts, spacing and radius. `tailwind.config` reads from it. Only head-of-design changes it.

Name tokens by role, not hue (`surface`, `surface-raised`, `text`, `text-muted`, `accent`, `danger`), so a rebrand changes one file.
