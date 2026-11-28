# Security lens

Look for **real trust-boundary failures**: who could do what they shouldn't, and how. On a Bet whose door is sign-in, money, personal data or secrets, this lens always runs and is never retired.

## Check

- **Secrets:** none in code, config, logs, client bundles, or `NEXT_PUBLIC_*` variables.
- **Auth:** every new route and server action checks who's calling, itself; admin is never protected by middleware alone; the session is signed and expires.
- **Input to output:**
  - user, scraped and model text is never put into HTML without sanitising;
  - JSON-LD goes through `lib/json-ld.ts`;
  - URLs from data go through `safe_url`;
  - SQL is parameterised.
- **Database access:** anon or public access is limited to the rows and columns the page needs; the service role is never used on a public path without size and rate limits.
- **Server-side fetches** of URLs from data or users: SSRF guard, no private IPs, redirects re-checked.
- **Cost and abuse:** public endpoints that write, send email, or call an LLM are rate-limited and size-capped.
- **CI and dependencies:** new workflows pin actions to a SHA, inputs go through `env:`, permissions are least-privilege. New dependencies are needed and pinned.
- **Headers** on public pages: HSTS and CSP don't regress.
- **Private error logging:** check the browser console as well as uncaught errors, using synthetic data. A generic error screen with no uncaught errors doesn't prove nothing private is logged. Don't forward raw exception text or stack traces until you've checked where they go.

In Claude Code, run the built-in `/security-review` as a second pass. Before a launch, or after a large change, recommend the `security-audit` skill (cloudflare/security-audit-skill) on a read-only copy, with no network. It's expensive, so the owner chooses the depth.

## In the report

For each issue: file:line, who can trigger it, what they gain, the smallest fix, and **Verified** or **Inferred**. A missing extra layer, where another layer already stops the attack, is a hardening note, not a blocker.
