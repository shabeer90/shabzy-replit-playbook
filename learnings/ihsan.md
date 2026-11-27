# Ihsan

- **What it is:** a multi-portal application with a private staff portal and public founder pages.
- **Stack:** React and TypeScript portals, an API with a database, built on Replit.
- **Where it runs:** Replit.
- **Dates:** November 2026.
- **Evidence:** the project's reports and tests, summarised here. The private material isn't copied or linked. Checks run locally don't prove the live release.

## 1. Check the production build, not just the dev server

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** two installed versions of the same dependency split a shared hook from its provider in the production bundle. Development checks passed, but replaying the served production bundle with synthetic API responses showed a blank page.
- **Impact:** a page that worked in development was blank in the production build.
- **Evidence:** the startup recovery report and the production-build browser checks that verified the local fix. Signed-in production wasn't verified.
- **Home:** [PLAYBOOK rule 17](../PLAYBOOK.md#1-the-rules); the QA agent refers to it.

## 2. Real integration tests with synthetic accounts

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** synthetic test accounts exercised real password checks, sessions, role revocation and database behaviour against non-production services. Mocked responses still covered the failures that need to be repeatable.
- **Impact:** login and access bugs that mocks can't show were testable without touching real data.
- **Evidence:** the access re-check report, the synthetic-login helper and the metrics tests. Fixtures were rolled back or cleaned up exactly, and security checks and rate limits stayed on. One helper first cleaned up rate-limit entries too broadly and was narrowed to the test's own entries; that first version isn't a pattern to copy.
- **Home:** [PLAYBOOK rule 18](../PLAYBOOK.md#1-the-rules); the CI baseline and QA agent refer to it.

## 3. Replit's preview proxy changes what the app sees

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** the preview proxy made repeated synthetic logins share one rate-limit bucket, and it added `noindex` headers to every page, public pages included. A test-only route for synthetic accounts fixed the logins without weakening password, session or rate-limit checks.
- **Impact:** QA logins hit rate limits, and the proxy's headers hid what the app itself sent.
- **Evidence:** the synthetic-login helper, crawler-control tests and the crawler report. App responses were checked directly, separately from the proxied ones. Platform behaviour may differ elsewhere (check current docs).
- **Home:** [PLAYBOOK section 11](../PLAYBOOK.md#11-replit-platform-notes).

## 4. Private screens left open after access changed

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** an open staff tab could keep showing confidential content after the user's access changed. Access is now re-checked, and private screens are hidden when the check fails or can't reach the server. Unsaved work survives only if the same account is confirmed.
- **Impact:** confidential records could stay visible to someone who'd lost access. This is fixed.
- **Evidence:** the access-fix verification and closure reports, with synthetic role changes and network-failure tests run locally. It favours privacy over offline use and doesn't promise instant revocation.
- **Home:** [the Admin row of the security baseline](../PLAYBOOK.md#5-security-baseline-check-before-launch), with an example under rule 6.

## 5. Keeping a private portal out of search

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** the staff portal got `noindex` in its first HTML and in its own response headers, and robots rules at the root of the host, scoped so the public founder pages stayed crawlable.
- **Impact:** the portal is kept out of search without hiding the public pages.
- **Evidence:** crawler-control tests and the login and crawler report, checked on local production builds. Live routing and headers were signed off separately. Robots rules aren't access control, and a disallow can stop a crawler from ever reading `noindex`.
- **Home:** [the SEO and GEO baseline](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 6. Editing the manifest didn't fix the dependency

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** a more specific pnpm override kept a vulnerable dependency installed after a broad override was changed.
- **Impact:** the fix looked done in `package.json` but wasn't in what was installed.
- **Evidence:** the dependency investigation and closure report. The installed versions and the audit were checked, and old lockfile findings were told apart from what was actually installed.
- **Home:** [the Supply chain row of the security baseline](../PLAYBOOK.md#5-security-baseline-check-before-launch).

## 7. Private error logging

- **When:** Nov 2026
- **Kind:** Held back
- **Home:** the general check is in the [security reviewer](../template/.claude/agents/security-reviewer.md). Details follow once it's fixed in Ihsan.

## 8. Metric labels must match what's counted

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** application submissions aren't unique startups, and distinct email addresses aren't verified people. The public labels had to match what was actually counted.
- **Impact:** without the fix, public numbers would have claimed more than they measured.
- **Evidence:** the metrics definitions and their tests, including case-insensitive email counting. These define how things are counted; they aren't audited totals. No live counts are included.
- **Home:** [PLAYBOOK rule 9](../PLAYBOOK.md#1-the-rules).

## 9. Replit's tools aren't installed skills

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** Replit gave its Agent built-in guidance for design, testing, deployment, workflows and read-only database checks. These aren't skills from the Skills CLI or Claude Code commands, and which tools worked changed from one task to the next.
- **Impact:** the team checked what was available each time, instead of assuming.
- **Evidence:** the platform instructions and the review reports. Specialised architecture and browser tools weren't available in a later review, and nobody claimed they ran.
- **Home:** [Replit's built-in guidance and tools](../SKILLS.md#replits-built-in-guidance-and-tools).

## 10. Review records say what was actually done

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** when the specialised tools weren't available, independent general agents read the code and ran Playwright, and the record named those methods and their limits.
- **Impact:** nobody mistook a reviewer's title for a review.
- **Evidence:** the review and QA reports. An earlier design consultation was kept separate, without claiming the same tools.
- **Home:** [Review records](../template/ORG.md#review-records).

## 11. Complete handoffs between agents

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** a scoped handoff carried the approved journey, design input, interfaces, privacy limits and acceptance checks in one place. The plan marked which deployment decision replaced an earlier recommendation.
- **Impact:** the agent doing the work didn't need to rediscover context or guess which decision stood.
- **Evidence:** the scoped task and the product plan. Advising didn't give permission to publish or change real records.
- **Home:** [Handing work to another agent](../template/ORG.md#handing-work-to-another-agent).

## 12. Separate verdicts for "works", "private" and "live"

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** the QA report kept real integration tests, mocked failures and production-build checks apart, and gave separate verdicts for what works, what's private and what's live. Signed-in live-release checks weren't claimed.
- **Impact:** a passing local build wasn't mistaken for a verified release.
- **Evidence:** the review and QA reports. A local staff journey didn't prove the investor journey, or that the live release had the reviewed build. This extends lessons 1 and 2.
- **Home:** [the QA report](../template/.claude/agents/qa-tester.md#report).
