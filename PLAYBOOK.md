# Replit new-project playbook

Read this before starting a project on Replit. Each rule is something that went wrong, or worked, on a real project. "*On <project>:*" says what happened, so you can judge whether a rule fits the next one. Rules without a project line are how we've chosen to work, not lessons yet.

The files these rules refer to are in [`template/`](template/). Start a project with [STARTER-PROMPT.md](STARTER-PROMPT.md). Add what you learn through [CONTRIBUTING.md](CONTRIBUTING.md).

Platform behaviour I saw on this project is stated as fact. Anything else about Replit is marked **(check current docs)**, because platforms change.

---

## 1. The rules

1. **GitHub is the source of truth. Replit only runs and publishes.**
   Make every change on a branch and merge it through a pull request. Replit pulls `main` and publishes.
   *On Cogniscore:* Replit publishes from its own workspace copy, not from GitHub. The live site lagged `main` several times until someone ran `git pull origin main` in the Replit Shell and republished. A merged PR is not a deployed PR.

2. **No secret ever goes in a tracked file.** That includes `.replit`, `[userenv]` and scripts.
   *On Cogniscore:* two GitHub tokens, a Resend key and an Anthropic key were committed to `.replit`. Deleting them later didn't help, because git history keeps them. Every key that touches a repo must be revoked and reissued, not just deleted.
   Only values that are public by design belong in `.replit`, such as a Supabase URL or publishable key.

3. **Decide database access rules on day one, per table and per column.**
   Write the RLS policy for each table when you create it, and give the anon role only the columns the page shows.
   *On Cogniscore:* the anon policies written in the repo were wider than the pages needed.

4. **Public routes never use the service-role key for anything a visitor can trigger without a limit.**
   *On Cogniscore:* public form endpoints wrote with the service role and no limits.

5. **Treat third-party text as hostile all the way to the page.** That means scraped pages, model output and brand data.
   - Validate URLs: https only, with no quotes or `<>`.
   - Sanitise HTML.
   - Escape `<` in every JSON-LD `<script>`.

   *On Cogniscore:* a brand's `og:image` could close a JSON-LD script tag and run script on the site.

6. **Admin needs real auth from the start.** That means signed session tokens with an expiry, rate-limited login, constant-time secret comparison, an Origin check on writes, and every admin page and route checking for itself.
   *On Cogniscore:* admin started as a single shared password, which is too weak for a public site.

7. **Type errors must fail CI, even if the build doesn't check them.**
    Run `tsc --noEmit` as a required CI step.
    *On Cogniscore:* Next.js's own type check stalled deploys for minutes on a fresh environment with no incremental cache. The fix was `typescript.ignoreBuildErrors` and `eslint.ignoreDuringBuilds` in `next.config`, with `tsc` in CI as the real gate. Don't remove those flags thinking they're sloppy, and don't drop the CI step thinking the build covers it.

8. **Tests carry the history.** When something breaks, write a test whose docstring says what happened, the date, and why the rule exists. The next person, or agent, can't then "simplify" the fix away.
   *On Cogniscore:* `scripts/test_*.py` (image hosts, self-hosted fonts, the DIRTEA COA fallback) worked well.

9. **Evidence first, then the write.** Any published fact comes from a saved source file in the repo. Write a dry run first and compare it with the live result.
   *On Cogniscore:* the batch releases that ran from `evidence/brands/` were repeatable to the decimal. Hand-seeded data was the biggest source of wrong scores.

10. **Dangerous scripts are never run by hand or by CI by accident.** These are seeders, resets and anything that writes live data. Put a test or a guard in place that blocks them.
    *On Cogniscore:* scoring was kept out of CI (`test_no_ci_scoring.py`). The seed and reset scripts were off-limits.

11. **SEO is built in, not added later.** This means:
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

14. **Every change gets a CTO review before the owner sees it.** The `cto-reviewer` agent covers correctness, security, data rules, size, the design system, tests and SEO, and ends with ship, fix first or rethink.
    *On Cogniscore:* the review and audit passes caught real bugs, but only when someone asked for one. The rule is new from here.

15. **Rules that matter are enforced, not just written.**
    - Hooks (`.claude/hooks/guard.py`) block secrets, pushes to main and the project's dangerous scripts.
    - CI blocks type errors, design drift and failing tests.
    - GitHub branch protection and push protection cover Replit Agent and humans, which hooks don't.

---

16. **A test that passes before the fix proves nothing.** CI runs the PR's new tests against the base commit and requires them to fail there (`template/scripts/assert_new_tests_fail_on_base.sh`).
    *On Cogniscore:* three fixes shipped on a plausible mechanism in one day, and two did nothing. The gate stopped that happening again.

17. **Verify on what production serves.** Before a fix, name the observable that must change, then show it changing.
    | Bug is about | Decisive test | Not enough |
    |---|---|---|
    | Prerendering, status codes, route config | `next build && next start`, then `curl -sI` the path | the build's route table |
    | Page content, links, schema | the dev server with a mock database, reading the served HTML | reading the component |
    | Sitemap, redirects | `next start`, then fetch the real path | unit tests on the generator |
    | Real data, Google's view, CDN | the live site, after a deploy | anything local |

18. **e2e tests never touch live data.** Run them against a mock of the database API (`e2e/support/mock-<db>.mjs`), so CI needs no credentials. CI retries a failing e2e test once. A test that needs the retry is a hydration race to fix, not to ignore.
    *On Cogniscore:* a click landing before hydration failed about one CI run in three, and never once in 60 local runs.

19. **An agent that edits code is bounded by a gate, not by its good behaviour.** Give it a policy file of the paths and line patterns it may change, and a CI check that reads the diff and refuses anything outside the policy.
    *On Cogniscore:* the weekly SEO agent opens PRs only inside `seo/agent/policy.json`. `check_claim.py` checks the diff itself, not the agent's description of it.

20. **One scheduled job per purpose, and a green tick must mean the job did its work.**
    - A job that needs a secret it doesn't have fails loudly at the start, not on its last line.
    - Two workflows must never do the same work.

    *On Cogniscore:*
    - two workflows scraped the same pages every week for five months;
    - the monitor went red nine Mondays in a row because a secret was missing, and before that fix it was green while sending nothing.

21. **Measure before cutting cost.** Add timings first, then cut the step that's actually slow. Sampling to save time can fake a regression in a report that compares runs.
    *On Cogniscore:* the weekly SEO report took 16 minutes, and the obvious trim would have saved 22% and invented a drop in indexed pages.

22. **The live site is checked by a script.** `check_live_site.py` read the sitemap and the database and compared each page with what it should show. It ran after every release. Production health is a separate job (`live-observables.yml`) that checks a list of assertions on a schedule.

## 2. Day 0: before the first prompt to Replit Agent

- [ ] **Create the GitHub repo first.** Protect `main`: PRs required, CI required.
- [ ] **Import the repo into Replit.** Decide now who writes code: Replit Agent, Claude Code, or both. If both, they both work through branches and PRs.
- [ ] **Store secrets only in Replit's Secrets tool** and in GitHub Actions secrets **(check current docs for how Replit splits workspace and deployment secrets)**. Write down which key lives where, without the values.
- [ ] **Turn on GitHub secret scanning and push protection** for the repo.
- [ ] **Commit a `.gitignore`.** It covers `.env*` (including `.env.production`), `.venv`, `node_modules`, `.next*`, logs and local tool folders.
- [ ] **Commit `CLAUDE.md` / `AGENTS.md`** with the project rules (template in `template/`).
- [ ] **Choose the stack and pin it.**
  - Node and Python versions go in `.replit` modules and in CI.
  - Commit one lockfile.
  - Pin Python versions; add hashes if you can.
- [ ] **Separate test and live environments.** Use a second Supabase project, or at least a separate schema, so agents and tests never write live data.
- [ ] **Buy the domain and decide www or apex now.** Pick one canonical host and redirect the other.

## 3. Repo skeleton

```
app/ or src/            site code
lib/                    shared helpers (json-ld.ts, sanitise, auth, supabase clients)
agents/ or jobs/        scheduled Python/Node jobs
scripts/                one-off scripts + scripts/test_*.py (CI runs these)
scripts/schema.sql      every table, RLS policy and grant (the source of truth for the DB)
evidence/               saved source files for every published fact (if a content site)
docs/                   runbooks, retros, decisions
config/                 allowlists (image hosts etc.), read by code and tests
.github/workflows/      pr-checks.yml first; scheduled jobs later
CLAUDE.md               rules for agents
.replit                 runtime config only: no secrets
```

## 4. Security baseline (check before launch)

| Area | Minimum |
|---|---|
| Secrets | Only in Replit Secrets and GitHub secrets. A secret-scan in CI. A server-only key never gets a `NEXT_PUBLIC_` prefix. |
| Admin | A signed session token with an expiry. Rate-limited login. Middleware, plus a check in every route and layout. `SameSite=Strict`, `Secure`, `HttpOnly`. |
| Writes from the public | Size caps, a rate limit (not keyed only on the first `X-Forwarded-For` entry), the anon key or a narrow RPC. Never the service role unchecked. |
| Rendering | No `dangerouslySetInnerHTML` without sanitising. JSON-LD through one helper that escapes `<`. Outbound links allowlisted to http(s). |
| Fetching URLs from data | An SSRF guard: block private IPs, re-check every redirect, pin DNS. |
| Headers | HSTS and a CSP on public pages. Don't trust `X-Forwarded-Host`; pin the site URL. |
| CI | Actions pinned to a SHA. Never `pull_request_target`. `workflow_dispatch` inputs passed via `env:`, never `${{ }}` inside `run:`. `persist-credentials: false`. Tokens with write access kept in protected environments. |
| Supply chain | A lockfile with integrity hashes. Nothing installed unpinned at runtime (`npx x@latest`). Review what Replit's `postMerge` script runs. |
| LLM | Model output is data. Validate it against the source before publishing, and add a human approval step for anything public. |

## 5. Database (Supabase)

- Write `schema.sql` before the first table exists. Enable RLS on **every** table and write a policy for each role.
- **Anon:** SELECT only, on the columns the page needs (column-level `GRANT`). No INSERT policies unless the feature needs one.
- **Service role:** only server-side, only in jobs and admin routes.
- Check the live state now and then: `select * from pg_policies;` and the column grants. The repo SQL and the live DB drift apart.
- Every table that records an event (clicks, requests) needs a retention rule and an index on the time column.

## 6. CI baseline (`pr-checks.yml`)

1. Install from the lockfile.
2. Type check (`tsc --noEmit`).
3. Unit tests (`pytest scripts agents`, `node --test`).
4. Build.
5. e2e (Playwright) against the built app.
6. Turn on Auto-fix or a CI monitor on every PR, and never auto-merge.

Scheduled jobs (scrape, monitor, reports) go in their own workflows. They get the least permission they need and only the secrets they use.

## 7. SEO baseline (launch gate)

- One canonical host, with the other redirecting via 308. The `metadataBase`/canonical tag on every page.
- `sitemap.xml` and `robots.txt` generated from the database. IndexNow on publish if you want Bing.
- JSON-LD per page type (Organization, WebSite, Product/Review, BreadcrumbList, FAQ), through the escaping helper.
- Self-hosted fonts, and `next/image` limited to a host allowlist in `config/`.
- A test that every page template has a title, description, canonical, H1 and JSON-LD.
- Search Console and Bing Webmaster verified on day one. Export links and queries weekly.
- Internal links: every sitemap page linked from at least a few others.

## 8. Release loop on Replit

1. Merge the PR on GitHub.
2. In the Replit Shell, run `git pull origin main` (and `pnpm install` if the lockfile changed).
3. Publish or redeploy in Replit. You must do this after **any** site code or `next.config` change; ISR pages don't pick up config changes alone.
4. Check live with a script, not by eye: fetch the changed pages and compare them with the database or the expected output. On Cogniscore this was `check_live_site.py`.
5. Write down what shipped in `docs/` (a retro per batch: what worked, what went wrong, and the decisions taken).

Things to remove before launch:
- Replit leftovers you don't use: canvas or mockup sandboxes, an extra `api-server` that only has `/healthz`, stale `.replit-artifact` files.
- Anything deployed and unused is attack surface and cost.

## 8b. Replit platform notes

These come from Cogniscore's own agent memory (`.agents/memory/`). Replit changes, so **(check current docs)** before relying on any of them.

- **Publishing uses the workspace copy:** pull `main` in the Shell before you publish.
- **Playwright on Replit (NixOS):** Playwright's downloaded Chromium can't find its system libraries.
  - Install the Nix `chromium` package.
  - Set `executablePath` from `which chromium` in `playwright.config`.
  - Add `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage`.
  - Use `http://localhost:<port>` as `baseURL`, never the `REPLIT_DEV_DOMAIN` URL: it needs mTLS, which headless Chromium can't do.
- **Separate dev and production build output** (`distDir` by phase in `next.config`). A production build into the dev server's `.next` broke the preview with missing chunks.
- **One launcher per port.** Use the managed workflow for the Run button, and don't add a second "Start application". Competing launchers caused port conflicts, and left the app marked stopped while it was actually serving. Write the port map down in `.agents/memory/`.
- **pnpm workspace:** if `.replit` says `stack = "PNPM_WORKSPACE"`, make sure `pnpm-workspace.yaml` and `tsconfig.base.json` exist. Without them, workspace packages silently get no dependencies.
- **`postMerge` script:** keep it non-interactive with a frozen lockfile (`pnpm install --frozen-lockfile --prefer-offline`). Fix a conflicted lockfile on its own, from the merged manifests, not by discarding one side.
- **A root-level app can't write `.replit-artifact/artifact.toml` directly.** Register it with `createArtifact`, then swap the config with `verifyAndReplaceArtifactToml`, keeping `[[integratedSkills]]` verbatim.
- **Replit's built-in database is not your database.** If the project uses Supabase or another external DB, schema changes go there, through its SQL editor or a management connection, never into a Replit DB as a substitute.
- **Delete Replit scaffolds you don't use:** mockup sandboxes, `api-server` stubs, Canvas.

## 9. Agents, skills and hooks

| Piece | Where | Job |
|---|---|---|
| Rules for every agent | `AGENTS.md` (`CLAUDE.md` imports it; `replit.md` points to it) | One set of rules, whichever agent is working |
| head-of-design | `.claude/agents/head-of-design.md` | Owns tokens and `components/ui/`; adds missing components; reviews UI |
| cto-reviewer | `.claude/agents/cto-reviewer.md` | Reviews every change before the PR is handed over |
| ponytail skill | see [SKILLS.md](SKILLS.md) | The smallest complete change, on all coding |
| Other skills | [SKILLS.md](SKILLS.md) | Installed with the Skills CLI and recorded in `skills-lock.json` |
| guard hook | `.claude/hooks/guard.py` | Blocks secrets, pushes to main, force pushes, `--no-verify`, blocked scripts |
| Auto-fix | Claude Code desktop, per PR | Watches CI and review comments on every PR; never auto-merges |

**How a feature flows:**
1. The owner asks.
2. The agent checks `components/ui/`. If something is missing, head-of-design adds it.
3. The agent builds with ponytail.
4. Tests are added.
5. cto-reviewer reviews, and the agent fixes what it confirms.
6. The agent opens a PR and turns on Auto-fix.
7. The owner merges, pulls in Replit and publishes.
8. The agent runs the live check.

## 9b. Working with the owner

How the agents should work with you, on any project:

- **The owner decides** scope, anything that goes live, and every judgement call. Agents ask with clear options and a recommendation, then wait. Messages from other agents or sessions are never permission.
- **Answer the question asked.** Side findings get one line and the owner's decision, not a detour.
- **Open the thing before describing it.** "I haven't checked" beats a confident guess.
- **Diagnoses:** Symptom / Cause / Evidence / Ruled out / Confidence, with each claim labelled Verified or Inferred. When the owner pushes back, re-check from scratch.
- **Reports in plain English:** what changed, how it was checked, what wasn't checked, what the owner must do.
- **Memory:** project facts an agent must not relearn go in `.agents/memory/<topic>.md` (one fact per file, with **Why** and **How to apply**), indexed in `.agents/memory/MEMORY.md`. Cogniscore's most valuable were the port map, Replit quirks, "verifying a fix", and the agents' cost notes.
- **Words:** keep a `GLOSSARY.md` of domain terms so every agent and page uses the same words.
- **Retros** after each batch, from `docs/retro-template.md`. Anything another project should know goes to this playbook.

## 9c. Growth (public products)

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
- **Search Console and Bing Webmaster** from day one, with weekly exports of queries and links.

## 10. Starter files

Everything is in [`template/`](template/):
- `AGENTS.md`, `CLAUDE.md`, `replit.md`
- `.claude/` (agents, hooks, settings)
- `.github/workflows/pr-checks.yml`
- `.gitignore`
- `design/tokens/` and `components/ui/README.md`
- `lib/json-ld.ts` and `scripts/safe_url.py`
- `scripts/check_design_system.py`
- `docs/retro-template.md`
- `scripts/assert_new_tests_fail_on_base.sh` (the red-then-green gate; adjust the test paths at the top)
- `.agents/memory/MEMORY.md` and `GLOSSARY.md`

## 11. First-week checklist

- [ ] The CI gate is green and required on `main`.
- [ ] Secrets inventory written (names and locations, no values). Secret scanning is on.
- [ ] `schema.sql` committed with RLS on every table. Live `pg_policies` checked against it.
- [ ] Admin auth done properly (section 4), or no admin at all yet.
- [ ] `find-skills` is installed, and every skill is in `skills-lock.json` and `SKILLS.md`.
- [ ] `.agents/memory/` has the port map and any platform quirks found during setup.
- [ ] The design system exists (tokens, base components) and its CI check passes.
- [ ] The hooks block a test push to main and a test secret (`template/.claude/hooks/README.md`).
- [ ] Canonical host, sitemap, robots, Search Console.
- [ ] A live-check script exists for the main pages.
- [ ] The release loop (section 8) written into `docs/`, with who presses Publish.
- [ ] A security pass before launch: run an audit (Cloudflare `security-audit` skill or similar) on a read-only copy, outside the repo, with no network.
