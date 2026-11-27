# Cogniscore (cogniscore.co.uk)

A UK site that scores mushroom and nootropic supplements on how completely brands disclose what's in them.

- **Stack:** Next.js 15, Tailwind, Supabase, Python agents in GitHub Actions, Claude for scoring and content, Resend for email.
- **Where it ran:** the site on Replit autoscale; jobs on GitHub Actions.
- **Dates:** May to Nov 2026.

## What went wrong

| When | What happened | Cost | Fix / rule |
|---|---|---|---|
| Nov | Live site behind `main` after merges | Fixes "shipped" but not live | PLAYBOOK rule 1; the release loop |
| Nov | `next/image` allowed any https host | Open image proxy; the busiest server path, at our cost | PLAYBOOK rule 11; host allowlist in `config/` |
| Jun–Nov | Hand-seeded data and model sub-scores published without the rubric | Scores couldn't be reproduced from the published rules | PLAYBOOK rule 9 |
| Nov | `next build` ignored type errors | Broken types reached main | PLAYBOOK rule 7 |
| Nov | Three fixes shipped on a plausible mechanism; two did nothing | Wasted deploys and false "fixed" reports | PLAYBOOK rules 16, 17; red-then-green CI gate |
| Jun–Nov | Two workflows scraped the same pages weekly | Double requests to every brand site | PLAYBOOK rule 20 |
| Sep–Nov | The monitor was green while sending nothing, then red nine weeks for a missing secret | Nobody noticed failures | PLAYBOOK rule 20 |
| Nov | e2e click raced hydration on CI only | About one CI run in three re-run | PLAYBOOK rule 18 |
| Nov | Next.js's type check stalled deploys | Deploy timeouts | PLAYBOOK rule 7 (corrected) |
| Nov | Playwright's Chromium failed on Replit's NixOS | e2e couldn't run on Replit | PLAYBOOK section 11 |
| Nov | Unused Replit leftovers (Canvas, an api-server with only `/healthz`) deployed | Attack surface and confusion | PLAYBOOK section 10 |

## What worked

- **Evidence files** (`evidence/brands/`) drove every data write. Batch releases matched their dry runs exactly.
- **One brand at a time**, checked live before the next.
- **Tests whose docstrings tell the story** (`scripts/test_*.py`), so fixes weren't undone.
- **A live-check script** (`check_live_site.py`) instead of checking by eye.
- **The owner decided every judgement call before anything was written.** The agent did the research and the dry runs.
- **Retros per batch** in `docs/`: outcome, what worked, what went wrong, decisions, still open.
- **Ponytail** for coding: small diffs, nothing extra.
- **Auto-fix on every PR:** the app watches CI and review comments.
- **A policy-gated SEO agent:** a weekly agent opens PRs, and a CI gate refuses anything outside its policy file.
- **Agent memory in `.agents/memory/`:** platform quirks and decisions, written once.
