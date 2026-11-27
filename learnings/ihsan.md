# Ihsan

Lessons approved for sharing from a multi-portal application, November 2026.
Evidence below describes project reports and tests reviewed for this contribution.
Those private materials are not copied here or linked as public evidence.
Local verification is not a claim that the live release was verified.

## 1. Production-built frontend checks

*On Ihsan:* different installed versions of a context-bearing dependency split a shared hook from its provider. Development checks passed, but replaying the served production bundle with synthetic API responses reproduced a blank page. Built-frontend browser checks verified the local repair.

Evidence reviewed: startup recovery report and production-frontend browser configuration. The report distinguishes local built-runtime verification from signed-in production verification.

Home: [PLAYBOOK rule 17](../PLAYBOOK.md#1-the-rules); the QA instructions refer to it.

## 2. Real non-production integration tests

*On Ihsan:* owned synthetic accounts exercised real password validation, sessions, role revocation and database behaviour against non-production services. Mocked browser fixtures covered deterministic failures alongside those integration tests.

Evidence reviewed: access-revalidation verification report, synthetic-login test helper and transactional metrics tests. Fixtures used exact cleanup or rollback; security checks and rate limits stayed enabled. A review reported overbroad development limiter cleanup, then narrowed the retained helper to exact test-owned entries. That deviation is not an approved cleanup pattern.

Home: [PLAYBOOK rule 18](../PLAYBOOK.md#1-the-rules); the CI baseline and QA instructions refer to it.

## 3. Preview proxy QA quirks

*On Ihsan:* preview IP handling made synthetic logins share rate-limit buckets. A reserved synthetic-account transport in the test harness used the real local development API without bypassing password, session or rate-limit checks. The proxy also added broad `noindex` headers, including on public pages.

Evidence reviewed: synthetic-login helper, crawler-control tests and crawler verification report. Direct app responses were checked separately from proxied responses. These are observed environment behaviours, not platform guarantees; current preview access requirements remain **(check current docs)**.

Home: [PLAYBOOK section 11](../PLAYBOOK.md#11-replit-platform-notes).

## 4. Cached private screen access

*On Ihsan:* an open staff tab could retain confidential content after access changed. Revalidation was changed to hide private screens on failed or unavailable verification, including network failure. Successful same-account checks preserved unsaved work.

Evidence reviewed: access-fix verification and closure reports. Synthetic role and credential changes, plus deterministic network-failure tests, exercised the boundary locally. The choice favours privacy over offline access; it does not promise instant revocation.

Home: [Admin security baseline](../PLAYBOOK.md#5-security-baseline-check-before-launch), with a short example under rule 6.

## 5. Private portal crawler controls

*On Ihsan:* the private staff portal needed initial HTML `noindex`, app-owned response directives and hostname-root robots rules scoped so public founder pages were not blocked.

Evidence reviewed: crawler-control tests and login/crawler verification report. Local built servers and direct app responses were checked. Full live routing and header sign-off remained separate. Crawling preferences are not authentication, and disallow alone can prevent a crawler reading `noindex`.

Home: [SEO baseline](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 6. Resolved dependency verification

*On Ihsan:* a more-specific pnpm override kept an affected dependency installed after a broad override changed. The edited manifest alone did not show remediation.

Evidence reviewed: dependency-resolution investigation and closure report. Installed resolution and the active dependency audit were checked; archived lockfile findings were distinguished from installed runtime dependencies.

Home: [Supply chain security baseline](../PLAYBOOK.md#5-security-baseline-check-before-launch).

## 7. Private error logging checks

*On Ihsan:* synthetic checks showed that a generic error fallback and no uncaught browser errors did not establish safe console logging.

Evidence reviewed: synthetic browser error-handling checks and their review summary. This was an unresolved logging limitation at contribution time, not evidence of real-data disclosure or external transmission. No affected-data details, private paths or reproduction payloads are included.

Home: [security reviewer](../template/.claude/agents/security-reviewer.md). This check is not assigned to a second reviewer.

## 8. Accurate public metric definitions

*On Ihsan:* application submissions were not unique startups, and distinct current primary email addresses were not verified people. Public labels needed to match those definitions.

Evidence reviewed: metrics contract and aggregate tests, including trimmed, case-insensitive primary-email counting. These establish counting definitions, not audited people totals. No live counts are included.

Home: [PLAYBOOK rule 9](../PLAYBOOK.md#1-the-rules); no separate metric policy was added.
