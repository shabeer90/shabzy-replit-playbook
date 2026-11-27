# Cogniscore

- **What it is:** a UK site (cogniscore.co.uk) that scores mushroom and nootropic supplements on how completely brands disclose what's in them.
- **Stack:** Next.js 15, Tailwind, Supabase, Python agents in GitHub Actions, Claude for scoring and content, Resend for email.
- **Where it runs:** the site on Replit autoscale; scheduled jobs on GitHub Actions.
- **Dates:** May to November 2026.
- **Evidence:** the project's tests, workflows, agent memory and batch retros. Security lessons that aren't fixed yet are left out.

## 1. A merged PR isn't a live PR

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** Replit publishes from its own workspace copy, so the live site stayed behind `main` after merges until someone pulled in the Replit Shell and republished.
- **Impact:** fixes were reported as shipped but weren't live.
- **Evidence:** live pages compared with `main` after several releases.
- **Home:** [PLAYBOOK rule 1](../PLAYBOOK.md#the-rules) and the [release loop](../PLAYBOOK.md#release-loop-on-replit).

## 2. The image optimiser was an open proxy

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** `next/image` allowed any https host, so anyone could use our server to fetch and resize any image.
- **Impact:** it was the busiest path on the server, at our cost.
- **Evidence:** the server's own analytics (3,479 hits on 20 Nov 2026, ahead of the homepage); fixed with a host allowlist and a test.
- **Home:** [PLAYBOOK rule 11](../PLAYBOOK.md#the-rules); host allowlist in `config/`.

## 3. Early scores couldn't be reproduced

- **When:** Jun to Nov 2026
- **Kind:** Went wrong
- **What happened:** hand-seeded data and model-written sub-scores were published before the rubric was applied in code.
- **Impact:** early scores couldn't be reproduced from the published rules. Fixed: every live product was rescored on a scorer that applies the rubric in code.
- **Evidence:** the project's read-only score audit on 27 Nov 2026. All 188 live products are on scorer 1.7 and match the rubric. The only findings were 11 products that aren't on the site.
- **Home:** [PLAYBOOK rule 9](../PLAYBOOK.md#the-rules).

## 4. Next.js's type check stalled deploys

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** on a fresh deploy with no incremental cache, the type check inside `next build` stalled for minutes. The build was set to skip it, and broken types then reached `main` until CI ran `tsc`.
- **Impact:** deploy timeouts first, then type errors on `main`.
- **Evidence:** deploy logs; the CI types step.
- **Home:** [PLAYBOOK rule 7](../PLAYBOOK.md#the-rules) (corrected in 1.1.0).

## 5. Fixes shipped that did nothing

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** three fixes shipped in one day on a plausible explanation; two of them changed nothing.
- **Impact:** wasted deploys and false "fixed" reports.
- **Evidence:** the before-and-after checks that showed no change; the red-then-green CI gate added afterwards.
- **Home:** [PLAYBOOK rules 16 and 17](../PLAYBOOK.md#the-rules); `template/scripts/assert_new_tests_fail_on_base.sh`.

## 6. Two jobs did the same work

- **When:** Jun to Nov 2026
- **Kind:** Went wrong
- **What happened:** two scheduled workflows scraped the same brand pages into the same table every week.
- **Impact:** double requests to every brand site for five months.
- **Evidence:** the workflow schedules and run history; a test now pins one job per purpose.
- **Home:** [PLAYBOOK rule 20](../PLAYBOOK.md#the-rules).

## 7. A green tick that meant nothing

- **When:** Sep to Nov 2026
- **Kind:** Went wrong
- **What happened:** the monitor ran green while sending nothing. Then it went red nine Mondays in a row because a secret was missing, and failed only on its last line.
- **Impact:** nobody noticed failures for weeks.
- **Evidence:** the workflow run history; a test now checks the job fails at the start when its secret is missing.
- **Home:** [PLAYBOOK rule 20](../PLAYBOOK.md#the-rules).

## 8. A hydration race only on CI

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** an e2e test clicked before the page had hydrated, so the click wasn't recorded. It failed on CI and never locally.
- **Impact:** about one CI run in three had to be re-run.
- **Evidence:** 60 clean local runs against the CI failure rate; the test was fixed to wait for hydration.
- **Home:** [PLAYBOOK rule 18](../PLAYBOOK.md#the-rules).

## 9. Playwright didn't run on Replit

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** Playwright's downloaded Chromium couldn't find its system libraries on Replit's NixOS.
- **Impact:** e2e tests couldn't run on Replit until Chromium came from Nix.
- **Evidence:** the error output and the working `playwright.config` change.
- **Home:** [Replit platform notes](../modules/replit-platform.md).

## 10. Unused Replit services

- **Kind:** Held back
- **Home:** [the PLAYBOOK release loop](../PLAYBOOK.md#release-loop-on-replit). Details follow once it's fixed in Cogniscore.

## 11. Evidence files drove every data write

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** each data release read from saved brand evidence files (`evidence/brands/`), not from memory or hand-seeding.
- **Impact:** every batch's live scores matched its dry run exactly.
- **Evidence:** dry run compared with live for each batch, recorded in the batch retros.
- **Home:** [PLAYBOOK rule 9](../PLAYBOOK.md#the-rules).

## 12. One brand at a time

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** releases went one brand at a time, each checked live before the next.
- **Impact:** every problem stayed small and traceable to one brand.
- **Evidence:** the batch retros.
- **Home:** [PLAYBOOK rule 12](../PLAYBOOK.md#the-rules).

## 13. Tests that tell the story

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** each bug fix got a test whose docstring says what happened, when and why.
- **Impact:** fixes weren't "simplified" away later.
- **Evidence:** `scripts/test_*.py` in the project.
- **Home:** [PLAYBOOK rule 8](../PLAYBOOK.md#the-rules).

## 14. A script checks the live site

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** after each release, `check_live_site.py` compared every sitemap page with what the database said it should show.
- **Impact:** release checks took one command, not checking by eye.
- **Evidence:** the script and its runs in the batch retros.
- **Home:** [PLAYBOOK rule 22](../PLAYBOOK.md#the-rules).

## 15. The owner decided, the agent prepared

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** every judgement call was put to the owner before anything was written. The agent did the research and the dry runs.
- **Impact:** no live change happened without a decision behind it.
- **Evidence:** the decisions sections of the batch retros.
- **Home:** [PLAYBOOK, working with the owner](../PLAYBOOK.md#working-with-the-owner).

## 16. A retro after every batch

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** each batch ended with a retro: outcome, what worked, what went wrong, decisions, still open.
- **Impact:** decisions and mistakes carried forward to the next batch.
- **Evidence:** the retros in the project's `docs/`.
- **Home:** `template/docs/retro-template.md`.

## 17. The smallest change that works

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** coding followed the ponytail skill: small diffs, nothing extra.
- **Impact:** diffs stayed small and quick to review.
- **Evidence:** not measured; the owner's experience across the project.
- **Home:** [SKILLS.md](../SKILLS.md).

## 18. Auto-fix on every PR

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** the Claude Code app watched CI and review comments on every PR and woke the agent to fix them.
- **Impact:** nobody polled CI by hand.
- **Evidence:** PR history.
- **Home:** [the PLAYBOOK CI baseline](../PLAYBOOK.md#ci-baseline-pr-checksyml).

## 19. An SEO agent bounded by a gate

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** a weekly SEO agent opened PRs, and a CI check read the diff and refused anything outside its policy file.
- **Impact:** the agent could run on a schedule without being trusted to behave.
- **Evidence:** `seo/agent/policy.json` and `check_claim.py` with their tests.
- **Home:** [PLAYBOOK rule 19](../PLAYBOOK.md#the-rules).

## 20. Agent memory written once

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** platform quirks and owner decisions were written to `.agents/memory/`, one topic per file.
- **Impact:** agents stopped relearning the port map and Replit quirks.
- **Evidence:** the memory files and their index.
- **Home:** [PLAYBOOK, working with the owner](../PLAYBOOK.md#working-with-the-owner); `template/.agents/memory/MEMORY.md`.

## 21. Analysis succeeded but the database rejected the result

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** the app accepted a supported extraction value, but a CHECK constraint in Supabase rejected it on save. Extraction and scoring had worked, so the save error first looked like an analysis failure.
- **Impact:** valid evidence couldn't be saved until a separate schema migration was applied.
- **Evidence:** `e2e/admin-text-evidence.spec.ts`, `e2e/admin-source-worker.spec.ts` and `scripts/test-evidence-rejection.sh` separate the save failure from extraction. They don't prove every live database has the same schema.
- **Home:** [the database baseline](../modules/database.md#database-supabase).

## 22. Specs written against live data, pushed without a PR

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** on 25 Nov, Replit Agent pushed eight commits of search work and specs straight to `main`, so CI never ran them. The specs searched for VYVE and Real Mushrooms, which were in the live catalogue but not in CI's mock.
- **Impact:** 13 to 14 browser tests failed on every PR after that, including ones that touched nothing in the browser, until the mock got the two brands.
- **Evidence:** Cogniscore PR #63: the four affected spec files went from 13 failed and 12 passed to 25 passed. The commit authors show Replit Agent. Whether `main` was protected at the time wasn't checked.
- **Home:** [PLAYBOOK rules 1 and 18](../PLAYBOOK.md#the-rules). The playbook didn't stop it because the guard hook binds Claude Code only. The check is now branch protection requiring a PR (Day 0), and `template/replit.md` (2.8.0) tells Replit Agent to work through PRs.

## 23. Search box showed text typed before hydration but ignored it

- **When:** Nov 2026
- **Kind:** Went wrong
- **Repeat of:** Cogniscore lesson 8.
- **What happened:** the server-rendered search box showed text typed before React hydrated, but the app never picked it up or asked for suggestions. A browser test that held back the bootstrap script reproduced it every time.
- **Impact:** a visitor on a slow start could lose their search with no error.
- **Evidence:** `e2e/search-suggestions.spec.ts` failed 3 of 3 runs on the base and passed 3 of 3 with the fix (Cogniscore PR #64). This checks the browser journey, not production traffic.
- **Home:** the first-render check in [the QA agent](../template/.claude/agents/qa-tester.md). Lesson 8 was a click; this was typing, which the QA list didn't name.

## 24. A third-party value reaching public pages

- **Kind:** Held back
- **Home:** [PLAYBOOK rule 5](../PLAYBOOK.md#the-rules).
