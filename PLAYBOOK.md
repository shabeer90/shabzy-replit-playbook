# Playbook

Read this before starting a project. Most rules are something that went wrong, or worked, on a real project. "*On <project>:*" says what happened, so you can judge whether a rule fits the next one. Rules without a project line are how we've chosen to work, not lessons yet.

- **Start a project:** [STARTER-PROMPT.md](STARTER-PROMPT.md).
- **Files:** in [`template/`](template/), including [ORG.md](template/ORG.md), which defines how the AI company is organised.
- **Skills:** [SKILLS.md](SKILLS.md).
- **Adding what you learn:** [CONTRIBUTING.md](CONTRIBUTING.md).

Behaviour of Replit, GitHub or Claude Code that wasn't confirmed on a project is marked **(check current docs)**. Platforms change.

---

## 1. The rules

Rule numbers are permanent. New rules are added at the end. A rule that turns out wrong is rewritten in place, with one line saying what changed.

1. **GitHub is the source of truth. Replit only runs and publishes.**
   Make every change on a branch and merge it through a pull request. Replit pulls `main` and publishes.
   *On Cogniscore:* Replit publishes from its own workspace copy, not from GitHub. The live site lagged `main` several times until someone ran `git pull origin main` in the Replit Shell and republished. A merged PR is not a deployed PR.

2. **No secret ever goes in a tracked file.** That includes `.replit`, `[userenv]` and scripts.
   *On an earlier project:* provider keys were committed to a Replit config file. Deleting them later didn't help, because git history keeps them. Every key that touches a repo must be revoked and reissued, not just deleted.
   Only values that are public by design belong in `.replit`, such as a Supabase URL or publishable key.

3. **Decide database access rules on day one, per table and per column.**
   Write the RLS policy for each table when you create it, and give the anon role only the columns the page shows.

4. **Public routes never use the service-role key for anything a visitor can trigger without a limit.**

5. **Treat third-party text as hostile all the way to the page.** That means scraped pages, model output and brand data.
   - Validate URLs: https only, with no quotes or `<>`.
   - Sanitise HTML.
   - Escape `<` in every JSON-LD `<script>`.

6. **Admin needs real auth from the start.** That means signed session tokens with an expiry, rate-limited login, constant-time secret comparison, an Origin check on writes, and every admin page and route checking for itself.
   *On Ihsan:* an open staff tab could keep confidential records visible after access changed. Live revalidation now hides them when verification fails, including offline failures (section 5).

7. **Type errors must fail CI, even if the build doesn't check them.**
   Run `tsc --noEmit` as a required CI step.
   *On Cogniscore:* Next.js's own type check stalled deploys for minutes on a fresh environment with no incremental cache. The fix was `typescript.ignoreBuildErrors` and `eslint.ignoreDuringBuilds` in `next.config`, with `tsc` in CI as the real gate. Don't remove those flags thinking they're sloppy, and don't drop the CI step thinking the build covers it.
   Was "the build must fail on type errors" until Cogniscore showed the build's own check stalled deploys.

8. **Tests carry the history.** When something breaks, write a test whose docstring says what happened, the date, and why the rule exists. The next person, or agent, can't then "simplify" the fix away.
   *On Cogniscore:* `scripts/test_*.py` (image hosts, self-hosted fonts, a brand scraper's COA fallback) worked well.

9. **Evidence first, then the write.** Any published fact comes from a saved source file in the repo. Write a dry run first and compare it with the live result.
   *On Cogniscore:* the batch releases that ran from `evidence/brands/` were repeatable to the decimal. Hand-seeded data was the biggest source of wrong scores.
   *On Ihsan:* metric definitions separated application submissions from unique startups, and distinct primary email addresses from verified people. Those labels are not interchangeable.
   *On Adam Accounting:* sitemap dates come only from editorial records; pages without one get no date, rather than the build date.

10. **Dangerous scripts are never run by hand or by CI by accident.** These are seeders, resets and anything that writes live data. Put a test or a guard in place that blocks them.
    *On Cogniscore:* scoring was kept out of CI (`test_no_ci_scoring.py`). The seed and reset scripts were off-limits.

11. **On a public site, SEO is built in, not added later.** This means:
    - one canonical host;
    - a sitemap;
    - JSON-LD;
    - self-hosted fonts;
    - an image optimiser limited to listed hosts, not `hostname: '**'`;
    - Search Console from day one.

    *On Cogniscore:* the wildcard image optimiser was the busiest path on the server, an open proxy paid for by us.

12. **One brand, batch or feature at a time, and check it live before the next.** Small releases kept every problem small.

13. **One design system, owned by head-of-design.**
    - Tokens live in `design/tokens/`, and components in `components/ui/`.
    - Pages use only those. A component that's missing is added there first, never built as a one-off in a page.
    - `scripts/check_design_system.py` fails CI on raw colours and arbitrary Tailwind values outside the design system.
    *On Cogniscore:* the colours lived in the Tailwind config, with no owner and no check. The rule is new from here.

14. **Every change is reviewed by the agents who own that area, never by the one who wrote it.** The reviewers are em, qa, cto, security, design, cmo and data (`template/ORG.md`). `.claude/reviewers.txt` says which ones a project has, and which paths wake each one. Each writes a verdict to `.reviews/<branch>.md`, and the guard hook blocks `gh pr create` until every required reviewer says `ship`. That makes the reviews automatic, not something anyone has to ask for.
    *On Cogniscore:* the security audit, the SEO audits and the data retros each found real problems, but only when someone asked. The rule is new from here.

15. **Rules that matter are enforced, not just written.**
    - Hooks (`.claude/hooks/guard.py`) block secrets, pushes to main and the project's dangerous scripts.
    - CI blocks type errors, design drift and failing tests.
    - GitHub branch protection and push protection cover Replit Agent and humans, which hooks don't.

16. **A test that passes before the fix proves nothing.** CI runs the PR's new tests against the base commit and requires them to fail there (`template/scripts/assert_new_tests_fail_on_base.sh`).
    *On Cogniscore:* three fixes shipped on a plausible mechanism in one day, and two did nothing. The gate stopped that happening again.

17. **Verify on what production serves.** Before a fix, name the observable that must change, then show it changing.
    | Bug is about | Decisive test | Not enough |
    |---|---|---|
    | Prerendering, status codes, route config | build and serve production output (`next build && next start` for Next.js), then check the path over HTTP | the build's route table |
    | Page content, links, schema | the served production output with synthetic data; read HTML and exercise client-rendered content in a browser | reading the component |
    | Client runtime, shared hooks, providers | a browser journey against the production bundle and server, exercising hooks beneath the real provider | a passing dev-server journey or build |
    | Sitemap, redirects | the production server, then fetch the real path | unit tests on the generator |
    | Real data, Google's view, CDN | the live site, after a deploy | anything local |

    Was "read page content on the dev server" until Ihsan showed the production bundle can break where the dev server works.
    *On Ihsan:* different dependency versions split a shared hook from its provider in the production bundle, despite passing development checks. Replaying the served bundle with synthetic responses reproduced the blank page. Built-frontend regression checks verified the local fix, not a signed-in live release.
    *On Impact Connect:* a direct-execution guard in an imported logo validator ran its CLI exit path after bundling and stopped the server. Moving the CLI into a separate entry point removed that startup path; source-module checks alone missed it.
    *On Personal Website:* Replit's dev workflow hid a hydration fallback that replaced prerendered content. The static artifact also had a blanket production rewrite alongside route-specific redirects; it was removed so the 404 catch-all could apply. The built-site trace showed the hydration issue, but live route status was not checked.

18. **e2e tests never touch production or live data.** Keep mocked database-API tests (`e2e/support/mock-<db>.mjs`) for fast, credential-free checks. Add controlled non-production integration tests when real passwords, sessions, roles or database behaviour matter.
    - Use a confirmed non-production service and database, with owned synthetic accounts and records only. Never write real customer records, even in development.
    - Roll back transactions or reliably clean up exact owned fixtures, including sessions and test-owned rate-limit entries, after success or failure. Never reset shared limits.
    - Keep authentication, authorisation and rate limits unchanged. Test transport isolation belongs in the test harness, never in production auth code.
    - CI retries a failing e2e test once. Investigate the cause. A passing retry doesn't clear the failure.

    *On Cogniscore:* a click landing before hydration failed about one CI run in three, and never once in 60 local runs.
    *On Ihsan:* synthetic accounts exercised real password validation, sessions and role revocation against the development API and database. Mocked browser responses remained useful for deterministic runtime failures.
    Was mock-only until Ihsan showed that real password, session, role and database checks needed controlled non-production integration tests.

19. **An agent that edits code is bounded by a gate, not by its good behaviour.** Give it a policy file of the paths and line patterns it may change, and a CI check that reads the diff and refuses anything outside the policy.
    *On Cogniscore:* the weekly SEO agent opens PRs only inside `seo/agent/policy.json`. `check_claim.py` checks the diff itself, not the agent's description of it.

20. **One scheduled job per purpose, and success must mean the work was done.**
    - A job that needs a secret it doesn't have fails loudly at the start, not on its last line.
    - Two workflows must never do the same work.
    - The same goes for any call that writes somewhere else (storage, email, payments, webhooks): check the returned result and report failure. A call that returned without throwing hasn't succeeded. Test the path where the provider returns an error.

    Was "a green tick must mean the job did its work" until Impact Connect and Adam Accounting showed request-path calls failing the same way.

    *On Cogniscore:*
    - two workflows scraped the same pages every week for five months;
    - the monitor went red nine Mondays in a row because a secret was missing, and before that fix it was green while sending nothing.

    *On Impact Connect:* a storage helper returns `false` on failure, so awaiting it proved nothing unless the caller checked the result.
    *On Adam Accounting:* the contact route awaited the email SDK but ignored its returned error. It now checks the result and rejects unsaved enquiries when the provider fails. Provider acceptance still doesn't prove the email arrived.

21. **Measure before cutting cost.** Add timings first, then cut the step that's actually slow. Sampling to save time can fake a regression in a report that compares runs.
    *On Cogniscore:* the weekly SEO report took 16 minutes, and the obvious trim would have saved 22% and invented a drop in indexed pages.

22. **The live site is checked by a script, not by eye.** After every release, a script compares each sitemap page with what the database says it should show. A separate scheduled job checks production health. List the command under *Live check* in `AGENTS.md`. Image checks fetch each published image URL and decode the bytes; a file existing, or an HTTP 200, isn't proof.
    Was "compare pages with the database" until Impact Connect showed an image file can exist while its public URL serves the wrong thing.
    *On Cogniscore:* `check_live_site.py` and `live-observables.yml`.
    *On Impact Connect:* the logo validator checked that files existed, not what the published image URLs returned, so it couldn't confirm the live site had no broken logos.

23. **Every project runs as an AI company.** The owner is the board. The main session is the CEO. The CPO, CTO and CMO and their teams are agents with one owner per job (`template/ORG.md`). No two agents do the same check.

24. **Reviews cost tokens, so they're scoped.** Reviewers wake only for their paths, and the retro records what each batch cost. The full budget is in `template/ORG.md`.

25. **A finding seen twice becomes a check.** A test, a hook rule or a CI step, so no reviewer has to spot it a third time. This is how the work gets cheaper and more autonomous from one project to the next.

26. **Autonomy is earned, one level at a time, and only the owner moves it.** The ladder, and what's never delegated, are in `template/ORG.md`.

27. **Words read like a person wrote them.** Every user-facing word, and every report to the owner, is plain and specific, with no AI tells. The CMO reviewer checks with the `humanizer` skill.
    *On Cogniscore:* drafts were rewritten for plain English again and again, by hand. The rule is new from here.

28. **The product looks agency-built, not AI-made.** head-of-design writes `design/DESIGN.md`, with real references and a point of view, before any component exists, using the `impeccable` skill. Generic AI patterns (purple gradients, glass cards, three equal icon cards, emoji icons, invented stats) are never the default.

29. **No PRD, no feature: the project is not a feature factory.**
    - `docs/ROADMAP.md` is the only list of what gets built, with at most three items under **Now**. Every other idea, including Replit Agent's suggestions, is parked with its source and date.
    - Anything bigger than a small fix needs a PRD that the leadership agents have reviewed and the owner has approved.
    - The guard hook won't open a PR without a link to an approved PRD, or `PRD: fix` for a small fix.

    *On the owner's Replit projects:* Replit kept suggesting features, and building them was tempting. Products drifted, and what was actually planned got forgotten.

30. **The user's end-to-end journey always works.**
    - `docs/JOURNEYS.md` lists the paths a user takes from start to done, each with an e2e test.
    - QA runs all of them on every PR that touches the app, and the EM won't sign off if one broke.
    - After a release, the CEO runs them against the live site.

    A feature that works on its own but breaks the journey is a failed feature.


## 2. How the company works

Each project is run as an AI company. [`template/ORG.md`](template/ORG.md) is the single source for:
- who owns what (the owner as board; the CEO, CPO, CTO, CMO and their teams);
- how work moves from ask to PRD to live;
- how the roadmap stops a feature factory;
- the token budget;
- the autonomy ladder.

The agent files are in [`template/.claude/agents/`](template/.claude/agents/), and ORG.md's roles table says which agent owns what.

What the guard hook blocks is listed in [`template/.claude/hooks/README.md`](template/.claude/hooks/README.md).

Hooks bind Claude Code only. If Replit Agent builds something, have Claude Code run the reviews on that branch before you merge.

## 3. Day 0: before the first prompt to an agent

- [ ] **Create the GitHub repo first.** Protect `main`: PRs required, CI required.
- [ ] **Import the repo into Replit.** Decide now who writes code: Replit Agent, Claude Code, or both. If both, they both work through branches and PRs.
- [ ] **Store secrets only in Replit's Secrets tool** and in GitHub Actions secrets **(check current docs for how Replit splits workspace and deployment secrets)**. Write down which key lives where, without the values.
- [ ] **Turn on GitHub secret scanning and push protection** for the repo.
- [ ] **Commit a `.gitignore`.** It covers `.env*` (including `.env.production`), `.venv`, `node_modules`, `.next*`, `.reviews/`, logs and local tool folders.
- [ ] **Commit `CLAUDE.md` / `AGENTS.md`** with the project rules (template in `template/`).
- [ ] **Choose the stack and pin it.**
  - Node and Python versions go in `.replit` modules and in CI.
  - Commit one lockfile.
  - Pin Python versions; add hashes if you can.
- [ ] **Separate test and live environments.** Use a second Supabase project, or at least a separate schema, so agents and tests never write live data.
- [ ] **Buy the domain and decide www or apex now.** Pick one canonical host and redirect the other.

## 4. Repo skeleton

```
app/ or src/            site code
lib/                    shared helpers (json-ld.ts, sanitise, auth, supabase clients)
agents/ or jobs/        scheduled Python/Node jobs
scripts/                one-off scripts + scripts/test_*.py (CI runs these)
scripts/schema.sql      every table, RLS policy and grant (the source of truth for the DB)
evidence/               saved source files for every published fact (if a content site)
config/                 allowlists (image hosts etc.), read by code and tests
.github/workflows/      pr-checks.yml first; scheduled jobs later
AGENTS.md, CLAUDE.md    rules for agents
ORG.md                  who owns what
design/DESIGN.md        the visual direction
docs/                   runbooks, retros, decisions
docs/prd/               PRDs (cpo writes; leadership reviews; owner approves)
docs/ROADMAP.md         the only list of what gets built
docs/JOURNEYS.md        the user journeys that must always work
.replit                 runtime config only: no secrets
components/ui/          shared components every page uses
design/tokens/          colour, type and spacing tokens
e2e/                    Playwright journeys
.agents/memory/         facts agents shouldn't relearn
GLOSSARY.md             the project's words
```

## 5. Security baseline (check before launch)

| Area | Minimum |
|---|---|
| Secrets | Only in Replit Secrets and GitHub secrets. A secret-scan in CI. A server-only key never gets a `NEXT_PUBLIC_` prefix. |
| Admin | A signed session token with an expiry. Rate-limited login. Middleware, plus a check in every route and layout. `SameSite=Strict`, `Secure`, `HttpOnly`. Re-check access when the user returns to the tab, reconnects, and every few minutes while it's open. While that check runs, or if it fails or can't reach the server, hide confidential screens, cancel private requests and clear private caches. Keep unsaved drafts only if the check confirms the same account. |
| Writes from the public | Size caps, a rate limit (not keyed only on the first `X-Forwarded-For` entry), the anon key or a narrow RPC. Never the service role unchecked. |
| Rendering | No `dangerouslySetInnerHTML` without sanitising. JSON-LD through one helper that escapes `<`. Outbound links allowlisted to http(s). |
| Fetching URLs from data | An SSRF guard: block private IPs, re-check every redirect, pin DNS. |
| Headers | HSTS and a CSP on public pages. Don't trust `X-Forwarded-Host`; pin the site URL. |
| CI | Actions pinned to a SHA. Never `pull_request_target`. `workflow_dispatch` inputs passed via `env:`, never `${{ }}` inside `run:`. `persist-credentials: false`. Tokens with write access kept in protected environments. |
| Supply chain | A lockfile with integrity hashes. Nothing installed unpinned at runtime (`npx x@latest`). Review what Replit's `postMerge` script runs. After a dependency fix, check what actually got installed and re-run the audit. A more specific pnpm override can beat a broad one, so editing `package.json` doesn't prove the fix. |
| LLM | Model output is data. Validate it against the source before publishing, and add a human approval step for anything public. |

*On Ihsan:* a range-specific pnpm override kept an affected dependency installed after a broad override was changed. What was actually installed, plus a clean audit, proved the fix. The edit didn't.

## 6. Database (Supabase)

- Write `schema.sql` before the first table exists. Enable RLS on **every** table and write a policy for each role.
- **Anon:** SELECT only, on the columns the page needs (column-level `GRANT`). No INSERT policies unless the feature needs one.
- **Service role:** only server-side, only in jobs and admin routes.
- Check the live state now and then: `select * from pg_policies;` and the column grants. The repo SQL and the live DB drift apart.
- Every table that records an event (clicks, requests) needs a retention rule and an index on the time column.

## 7. CI baseline (`pr-checks.yml`)

1. Install from the lockfile.
2. Type check (`tsc --noEmit`).
3. Unit tests (`pytest`; add `node --test` if the project has Node unit tests).
4. Build.
5. New tests must fail on the base commit (rule 16).
6. e2e (Playwright) against the built app, using the test modes and safeguards in [rule 18](#1-the-rules).
7. The day-one checks from `template/`, each written after the same mistake reached more than one project:
   - **e2e on the built app:** `playwright.config.ts` serves the production output, and `scripts/test_release_guards.py` fails if it points at a dev server (rule 17);
   - **bundle:** `scripts/check_bundle.py` fails when a public entry statically imports private code or goes over the JavaScript budget in `config/bundle.json` (Vite; other frameworks swap in their own check);
   - **external writes:** `scripts/check_external_writes.py` fails when a known provider write isn't wrapped in `checked()` from `lib/checked.ts` (rule 20). Add the project's providers to its list.
8. Turn on Auto-fix or a CI monitor on every PR. Don't auto-merge unless the project's autonomy level allows it (`template/ORG.md`).

For apps with split routes, check the built manifest's transitive static imports. Private routes must stay out of the public entry graph, and protected screens out of the login graph. Server-only page registries must stay out of the browser graph; an SSR conditional in the source doesn't prove the imports' side effects are gone. Set a JavaScript size budget for the project and fail the check when the built JavaScript exceeds it. Deferring code is not access control; private APIs still need authentication.

*On Impact Connect:* `tests/routeBundles.check.mjs` checks the emitted Vite graph and a 1.25 MiB JavaScript budget. It guards route boundaries and bundle size, not live page speed.

*On Adam Accounting:* moving eager SSR page imports into a separate server-only module reduced initial browser JavaScript from about 428KB to 198KB. The shared module's SSR conditional had not kept import side effects out of the browser bundle.

**Optional for public sites: performance budgets.** Run Lighthouse against the production build, on mobile and desktop, several times each, with a pinned Lighthouse version. Fail on the project's own score, layout-shift and JavaScript budgets. A mobile speed fix must be checked on desktop too. Local results are not live results (rule 17), and a failing budget is fixed, not loosened.

*On Adam Accounting:* critical CSS meant for the mobile homepage also applied on desktop and caused layout shifts ([lesson 1](learnings/adam-accounting.md#1-a-mobile-speed-fix-changed-the-desktop-layout)).

Scheduled jobs (scrape, monitor, reports) go in their own workflows. They get the least permission they need and only the secrets they use.

## 8. SEO and GEO baseline (public sites, launch gate)

- One canonical host, with the other redirecting via 308. The `metadataBase`/canonical tag on every page.
- `sitemap.xml` and `robots.txt` generated from the database. IndexNow on publish if you want Bing. Source sitemap modification dates from actual content records; omit optional dates when none exist, rather than substituting the build time (rule 9).
- JSON-LD per page type (Organization, WebSite, Product/Review, BreadcrumbList, FAQ), through the escaping helper.
- Self-hosted fonts, and `next/image` limited to a host allowlist in `config/`.
  Check that the required font files ship in the production output. For generated graphics, load those files in the renderer and wait for fonts before capture.
  *On Impact Connect:* the poster renderer needed production font paths, embedded WOFF2 files and `document.fonts.ready`. The source fix alone did not prove the fonts shipped or rendered correctly in a live release.
- A test that every page template has a title, description, canonical, H1 and JSON-LD.
- Response headers, checked separately from the HTML: compression on text responses, long caching for fingerprinted assets, revalidation for HTML. Check the production server and the published site separately (rule 17). Use the host's own settings where they're enough ([Adam Accounting lesson 3](learnings/adam-accounting.md#3-correct-html-did-not-establish-correct-file-delivery)).
- Search Console and Bing Webmaster verified on day one. Export links and queries weekly.
- Internal links: every sitemap page linked from at least a few others.
- Missing image paths return a real 404, with `Cache-Control: no-store`, not the SPA's HTML.
  *On Impact Connect:* missing uploads could fall through to the application response. Explicit missing-asset handling now returns 404 without caching; that doesn't tell us what browsers had already cached.
- Social preview tags use absolute HTTPS image URLs and a raster format supported by the target sharing services. Fetch and decode the image, check its intended dimensions, and compare Open Graph, Twitter and JSON-LD references.
  *On Impact Connect:* generated blog previews needed a PNG derivative and absolute metadata URLs. The production-bundle smoke test decodes a 1200×630 PNG and checks that the references agree.
- For AI assistants (GEO), each page answers its main question plainly near the top, with specific, attributed facts. AI crawlers are allowed in `robots.txt` unless the owner decides otherwise.
- Public article text, public profile content and displayed statistics are available in initial HTML without JavaScript. Use the same public data and access rules for ordinary visitors and crawlers, including unfamiliar user agents. Test the served content, not just metadata or an excerpt.
  *On Impact Connect:* full article and public founder content replaced incomplete crawler output, with statistics from the API's shared cache. HTTP checks cover ordinary visitors and named and unknown crawlers; they do not prove indexing or rankings.

**Private portals are an exception to the public indexing baseline.** Put `noindex` in initial HTML before JavaScript and in app-owned response directives (`X-Robots-Tag`), including app-controlled redirects and errors. Set crawler rules at hostname-root `/robots.txt`, not just inside a portal subpath. Scope them to private routes on a shared host, so the public pages stay crawlable; blanket disallow belongs only on wholly private hosts. Keep private URLs out of public sitemaps.

Crawler instructions are not access controls. Protected routes still need authentication. Disallowing a crawl can stop the crawler reading `noindex`; a blocked URL may still appear in search. Neither directive guarantees immediate removal.

*On Ihsan:* the private staff portal needed its own initial HTML and response directives, with root robots rules scoped so its public pages stayed crawlable.

## 9. Writing and design quality

**Writing (every project).** The test is whether a busy person would read it once and understand it.
- Short sentences, the reader's words, numbers instead of adjectives.
- No AI tells (the list is in `template/.claude/agents/cmo-reviewer.md`).
- The `humanizer` skill rewrites a draft; the CMO reviewer checks every user-facing change. The project's voice is in `AGENTS.md`.

**Design (anything with a UI).** The test is whether it could pass as the work of a good agency for this specific client.
- `design/DESIGN.md` first: audience, one feeling, three named reference sites, type, colour, grid, motion, what the brand never does. The owner approves it.
- Real content and data in every design, never filler.
- Restraint on screens people work in; a point of view on pages that persuade.
- `impeccable` for craft and critique, `ui-ux-pro-max` for palette and type data, `web-design-guidelines` for accessibility.

## 10. Release loop on Replit

1. Merge the PR on GitHub.
2. In the Replit Shell, run `git pull origin main` (and `pnpm install` if the lockfile changed).
3. Publish or redeploy in Replit. You must do this after **any** site code or `next.config` change; ISR pages don't pick up config changes alone.
4. Run the live-check script (rule 22).
    - For static artifacts, check `.replit-artifact/artifact.toml` and `public/_redirects` together; test both a known route and an unknown path over HTTP.
    - If the Replit dev workflow renders client-only pages but the published artifact is prerendered, test hydration in a browser against the built artifact too.
5. Write down what shipped in `docs/` (a retro per batch: what worked, what went wrong, and the decisions taken).

Things to remove before launch:
- Replit leftovers you don't use: canvas or mockup sandboxes, an extra `api-server` that only has `/healthz`, stale `.replit-artifact` files.
- Anything deployed and unused is attack surface and cost.

## 11. Replit platform notes

These are project observations from Cogniscore, Ihsan, Impact Connect and Adam Accounting, not platform guarantees. Replit changes, so **(check current docs)** before relying on them.

- **Publishing uses the workspace copy:** pull `main` in the Shell before you publish.
- **Uploaded assets need durable storage:** do not treat the published filesystem as the permanent copy. Await the storage write and check its result before reporting that an upload is durable. If it fails, report failure or clearly mark the upload as not backed up; retries alone are not success.
  *On Impact Connect:* logo paths depended on uploaded files. Backup calls were made awaitable with retries, but the helper still returns `false` when they fail, so callers must handle that result. This is not evidence that every production logo is backed up.
  [Replit's current guidance](https://docs.replit.com/build/troubleshooting) says published filesystems are not persistent; use [App Storage](https://docs.replit.com/features/data-and-storage/object-storage) or another durable store for uploads (checked 27 Nov 2026).
- **Playwright on Replit (NixOS):** Playwright's downloaded Chromium can't find its system libraries.
  - Install the Nix `chromium` package.
  - Set `executablePath` from `which chromium` in `playwright.config`.
  - Add `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage`.
  - Prefer `http://localhost:<port>` for isolated app checks. Cogniscore recorded a preview access problem attributed to mTLS; that is not a blanket restriction on headless preview access. Ihsan ran browser checks through its preview proxy. Current preview authentication and any mTLS requirement depend on the environment **(check current docs)**.
- **Preview proxy and synthetic QA:** check what reaches the app before assuming a browser-supplied client IP isolates a login bucket. Keep reserved synthetic-account transport inside the non-production test harness, targeting the real local API with unchanged password, session and rate-limit checks (rule 18). Never route real-user credentials this way, weaken production authentication, or raise, disable or globally reset limits to pass QA.
  *On Ihsan:* preview IP handling made repeated synthetic logins share a rate-limit bucket. A test-only local transport isolated those logins without changing application security.
- **Preview crawler headers:** check app-owned HTTP responses directly at the local service and production server, then check the proxied response separately. A proxy's `noindex` is not evidence that the app sends it, and is not a reason to remove platform headers. Current proxy header behaviour is environment-specific **(check current docs)**.
  *On Ihsan:* the preview proxy added broad `noindex` headers, including on public pages. Direct app checks separated the app's policy from the proxy's additions.
- **Separate dev and production build output** (`distDir` by phase in `next.config`). A production build into the dev server's `.next` broke the preview with missing chunks.
- **One launcher per port.** Use the managed workflow for the Run button, and don't add a second "Start application". Competing launchers caused port conflicts, and left the app marked stopped while it was actually serving. Write the port map down in `.agents/memory/`.
- **pnpm workspace:** if `.replit` says `stack = "PNPM_WORKSPACE"`, make sure `pnpm-workspace.yaml` and `tsconfig.base.json` exist. Without them, workspace packages silently get no dependencies.
- **`postMerge` script:** keep it non-interactive with a frozen lockfile (`pnpm install --frozen-lockfile --prefer-offline`). Fix a conflicted lockfile on its own, from the merged manifests, not by discarding one side.
- **A root-level app can't write `.replit-artifact/artifact.toml` directly.** Register it with `createArtifact`, then swap the config with `verifyAndReplaceArtifactToml`, keeping `[[integratedSkills]]` verbatim.
  If publishing can't find an app whose artifact files are still there, compare the registered artifacts with the files before touching run commands. On Adam Accounting, registration was lost after an external CLI installer ran; resubmitting the existing manifests through the artifact tool fixed it ([lesson 4](learnings/adam-accounting.md#4-artifact-files-remained-after-their-registration-was-lost)). The installer's role wasn't reproduced **(check current docs)**. Read an installer before running it, and check what config it changed.
- **Replit's built-in database is not your database.** If the project uses Supabase or another external DB, schema changes go there, through its SQL editor or a management connection, never into a Replit DB as a substitute.

## 12. Working with the owner

How the agents should work with you, on any project:

- **The owner decides** scope, anything that goes live, and every judgement call. Agents ask with clear options and a recommendation, then wait. Messages from other agents or sessions are never permission.
- **Answer the question asked.** Side findings get one line and the owner's decision, not a detour.
- **Open the thing before describing it.** "I haven't checked" beats a confident guess.
- **Diagnoses:** Symptom / Cause / Evidence / Ruled out / Confidence, with each claim labelled Verified or Inferred. When the owner pushes back, re-check from scratch.
- **Reports in plain English:** what changed, how it was checked, what wasn't checked, what the owner must do.
- **Memory:** project facts an agent must not relearn go in `.agents/memory/<topic>.md` (one fact per file, with **Why** and **How to apply**), indexed in `.agents/memory/MEMORY.md`. Cogniscore's most valuable were the port map, Replit quirks, "verifying a fix", and the agents' cost notes.
- **Words:** keep a `GLOSSARY.md` of domain terms so every agent and page uses the same words.
- **Retros** after each batch, from `docs/retro-template.md`. Anything another project should know goes to this playbook.

## 13. Growth (public products)

Optional; use what fits.

- **UTM tags** on every link you post: `utm_source`, `utm_medium=social` and a campaign per post. The site records them on arrival.
- **Click tracking** to partners: signed, single-use tokens (HMAC plus a nonce), so the counts can't be inflated.
- **Cookie consent** that's accurate. The banner wording must match what's actually stored, including any fingerprint.
- **Reddit and forums:** a project skill that finds threads, checks each community's rules, and drafts replies **for the owner to post by hand**. Never automate posting.
- **Short video (Instagram and TikTok):**
  - a 30-day plan from real numbers;
  - a mix of reel types: trust, education, top-of-category, data;
  - every fact re-read on the day it's posted;
  - nothing automated until a few reels have worked.

  *On Cogniscore:* `social/30-day-plan.md`.

## 14. Starter files

Everything is in [`template/`](template/). The README lists [each file and what it's for](README.md#the-template-file-by-file).

## 15. First-week checklist

- [ ] The CI gate is green and required on `main`.
- [ ] Secrets inventory written (names and locations, no values). Secret scanning is on.
- [ ] `schema.sql` committed with RLS on every table. Live `pg_policies` checked against it.
- [ ] Admin auth done properly (section 5), or no admin at all yet.
- [ ] `find-skills` is installed, and every skill is in `skills-lock.json` and `SKILLS.md`.
- [ ] `.agents/memory/` has the port map and any platform quirks found during setup.
- [ ] The design system exists (tokens, base components) and its CI check passes.
- [ ] The hooks block a test push to main, a test secret, and a PR with no reviews (`template/.claude/hooks/README.md`).
- [ ] `.claude/reviewers.txt` lists the right reviewers and paths for this project.
- [ ] `design/DESIGN.md` approved; voice written in `AGENTS.md`.
- [ ] `docs/ROADMAP.md` has the first three items under **Now**, each with an approved PRD; `docs/JOURNEYS.md` lists the core journeys, each with an e2e test.
- [ ] Canonical host, sitemap, robots, Search Console.
- [ ] A live-check script exists for the main pages.
- [ ] The release loop (section 10) written into `docs/`, with who presses Publish.
- [ ] A security pass before launch: run an audit (Cloudflare `security-audit` skill or similar) on a read-only copy, outside the repo, with no network.
