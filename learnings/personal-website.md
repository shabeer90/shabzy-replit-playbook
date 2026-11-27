# Personal Website

- **What it is:** a public portfolio built and deployed as a Replit static artifact.
- **Stack:** React, TypeScript, Vite, Tailwind CSS and static prerendering.
- **Where it runs:** Replit.
- **Dates:** June to November 2026.
- **Evidence:** local source, Git history and a browser trace against the built artifact; live deployment behaviour was not verified.

## 1. Replit's dev workflow can hide hydration failures

- **When:** Sep 2026
- **Kind:** Went wrong
- **What happened:** the Replit dev workflow used client-only rendering, while the published artifact contained prerendered HTML. In the built site, a lazy route's client Suspense fallback replaced that HTML during hydration. The skip link and Suspense boundaries were aligned between server and client.
- **Impact:** hydration recovery replaced the rendered page and caused a recorded layout shift. Matching both trees removed the recovery error and shift.
- **Evidence:** commit `1b5b42c`; `src/entry-server.tsx` and `src/main.tsx`. A browser trace against the built site showed the mismatch and layout shift; it does not establish that the reviewed change was deployed live.
- **Home:** [PLAYBOOK section 10](../PLAYBOOK.md#10-release-loop-on-replit), built-artifact verification.

## 2. Check Replit artifact rewrites against app redirects

- **When:** Sep 2026
- **Kind:** Went wrong
- **What happened:** `.replit-artifact/artifact.toml` had a blanket production rewrite from every path to `/index.html`, while `public/_redirects` defined a 404 catch-all for unknown routes. The Replit artifact rewrite was removed so route-specific rules could apply.
- **Impact:** the broad rewrite conflicted with the intended 404 behaviour for unknown paths. The configuration fix is visible in source, but the live HTTP status was not verified.
- **Evidence:** commits `3fd5ecd` and `a4f85f5`; `.replit-artifact/artifact.toml` and `public/_redirects`.
- **Home:** [PLAYBOOK section 10](../PLAYBOOK.md#10-release-loop-on-replit), static artifact routing checks.
