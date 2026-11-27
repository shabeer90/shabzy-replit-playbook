# Changelog

## 2.6.0 (27 Nov 2026)

- **Rule 20 widened, not a new rule:** success must mean the work was done, for any call that writes somewhere else (storage, email, payments, webhooks), not only scheduled jobs. Cogniscore, Impact Connect and Adam Accounting each hit a version of this.
- **STARTER-PROMPT:** checks Day 0 first, fills every placeholder including CI, matches reviewer paths to the repo, clears unused Replit scaffolds, proves the built app with one journey test, decides where uploads live, and ends with a definition of done. It says the hooks and review agents bind Claude Code only.
- **Proofread:** fixed rule references (CONTRIBUTING, QA), reviewer scope wording (QA, CLAUDE.md, README), who runs the PRD review (CPO, PRD template), and removed guidance kept in two places (guard list, AI tells, live check, Replit scaffolds, Search Console, tokens, section 14). The repo skeleton lists every template folder. Learnings may give a month range in **When**.
- **Upgrade from 2.5.x (optional):** check every external write in your project returns and reports failure (rule 20).

## 2.5.0 (27 Nov 2026)

- **Impact Connect, lessons 8–12:** publication-safe autofill, form refetch races, optional enrichment failures, actual zoom checks and fonts in generated graphics.
  QA gains a "Feature-specific cases" list; PLAYBOOK section 8 gains a packaged-font check.
- **Personal Website, lessons 1–2:** Replit's dev workflow hid a hydration failure that only the built artifact showed, and a blanket artifact rewrite overrode the site's 404 rule. Rule 17 gains the example; the section 10 release loop gains both checks.
- **Adam Accounting, lessons 1–11:** a mobile speed fix that broke desktop, SSR imports left in the browser bundle, compression and cache headers, lost artifact registration, unchecked email results, sitemap dates, filled-field readability, SEO warning triage, search titles vs headlines, unstyled first paint and ARIA roles.
  Examples extend rules 9 and 30 and sections 7, 8 and 11. QA checks the first render and filled form fields; the CMO records justified non-fixes and keeps search titles apart from headlines; design checks ARIA fits the element's role.
- **CONTRIBUTING:** a lesson must say what the next build does differently, and what its evidence leaves unverified.
- **Upgrade from 2.4.x (optional):** copy the QA, CMO and design checklist additions where they fit, plus the section 8 font and delivery checks. For static Replit artifacts, test a known and an unknown route over HTTP, and check hydration against the built artifact. No rules, roles, skills, hooks or CI changed.

## 2.4.1 (27 Nov 2026)

- README: each project's lessons come back with evidence of what worked, what failed and what to do differently, and the test is whether the same mistakes stop. No workflow or upgrade changes.

## 2.4.0 (27 Nov 2026)

- **SKILLS.md:**
  - adds the core `caveman` skill (juliusbrussee/caveman), pinned to a commit, for shorter chat replies; written work stays in plain prose;
  - lists the Caveman CLI under "Looked at, not chosen", with the reasons.
- **Upgrade (optional):** `npx skills add juliusbrussee/caveman --skill caveman`, then check `skills-lock.json` records it.

## 2.3.1 (27 Nov 2026)

- Proofread after the Impact Connect lessons: README lists all three projects and every template file; changelog wording no longer points at unfixed issues; patch versions defined; consistency fixes across learnings, QA verdicts, ROADMAP and SKILLS.

## 2.3.0 (27 Nov 2026)

- Seven approved Impact Connect lessons: CLI isolation in bundled servers, confirmed upload backups, decoded production image checks, missing-asset responses, raster social previews, initial public HTML and built route-graph checks. Raw evidence and limits are in `learnings/impact-connect.md`; examples extend rules 17 and 22, and checklists extend sections 7, 8 and 11.
- **Upgrade from 2.2.x (optional):** adopt the new route-graph, public-content, image-response, social-preview and upload-durability checks where they apply. No rule numbers, reviewers, skills, hooks or CI changed, so each project wires up the checks that fit it.

## 2.2.3 (27 Nov 2026)

- README: the template list now covers every folder, the intro mentions Ihsan, and "each rule" is now "most rules".

## 2.2.2 (27 Nov 2026)

- Cogniscore lesson 3 marked fixed, with the audit that shows it. Lesson 10 held back until it's fixed.

## 2.2.1 (27 Nov 2026)

- Proofread: fixed contradictions (who moves a PRD to Shipped, who keeps the roadmap, merging vs the autonomy ladder, live data writes at level 3, where the review file goes, model per role); one owner for each `code-review`; project stories moved out of SKILLS.md; rule 22 made general; role table and token budget no longer copied into PLAYBOOK; a cost section in the retro template; project details removed from the test-gate script; small wording fixes.
- Bug fix: `guard.py` now also blocks `git push origin HEAD` while on `main`, which it was always meant to. Nothing changes for correct use.

## 2.2.0 (27 Nov 2026)

- **One format for learnings files:**
  - `learnings/_template.md` sets an About block plus numbered lessons, each with When, Kind, What happened, Impact, Evidence and Home;
  - `cogniscore.md` and `ihsan.md` are converted to it (lesson numbers in `ihsan.md` unchanged);
  - CONTRIBUTING describes the format.
- **`CONTRIBUTE-PROMPT.md`:** adds a project's lessons in that format; linked from the README and CONTRIBUTING.

## 2.1.1 (27 Nov 2026)

- `UPGRADE-PROMPT.md`: brings an existing project up to the latest version. Linked from the README.

## 2.1.0 (27 Nov 2026)

- Four further approved Ihsan lessons: distinguish Replit-provided guidance from installed skills in `SKILLS.md`; record actual review methods and bounded specialist handoffs in `template/ORG.md`; separate implementation, privacy and live-release evidence in the QA report. Raw entries extend `learnings/ihsan.md`.
- **Upgrade from 2.0.0 (optional):** copy the new QA report and the handoff and review-record sections of `ORG.md`. Nothing enforced changed: no new rules, reviewers, skills, hooks or CI.

## 2.0.0 (27 Nov 2026)

- Eight approved Ihsan lessons: production-bundle checks (rule 17), controlled non-production integration tests (rule 18), preview proxy QA, cached private-screen access, private crawler controls, resolved dependency verification and accurate metric labels (a ninth is held back). Raw evidence summaries are in `learnings/ihsan.md`.
- **Upgrade from 1.1.x:** use the amended rules 17 and 18 and CI baseline when configuring QA. Adopt the Admin, Supply chain and private-portal SEO baseline changes where applicable. Update the QA and security reviewer files from `template/.claude/agents/`. Reviewer ownership, numbered rules, hooks and CI behaviour are unchanged.

## 1.1.2 (27 Nov 2026)

- Project details removed from security lessons that aren't fixed yet in the project they came from: rule 2 is made general, the project lines on rules 3 to 6 and their learnings rows are removed, and two template comments are made general. They come back once fixed. A brand name is removed from rule 8.

## 1.1.1 (27 Nov 2026)

- README rewritten in plain English.

## 1.1.0 (27 Nov 2026)

- **The AI company (`template/ORG.md`):**
  - the owner as board, plus CEO, CPO, CTO and CMO and their teams, one owner per job;
  - the feature flow;
  - the token budget;
  - the autonomy ladder.
  - New agents: `cpo` and `cmo-reviewer` (which replaces `seo-geo-reviewer`, adding copy review).
- **No feature factory (rules 29 and 30):**
  - `docs/ROADMAP.md` (three items under Now at most; every other idea, including Replit's suggestions, is parked);
  - PRDs reviewed by the leadership agents and approved by the owner (`docs/prd/`);
  - `docs/JOURNEYS.md`, with QA running every journey on every PR.
  - The hook blocks a PR without an approved PRD or `PRD: fix`.
- **Reviews:** em, qa, cto, security, design, cmo and data. They're path-scoped in `.claude/reviewers.txt`, and the hook blocks `gh pr create` until every required reviewer signs off.
- **Writing and design quality:**
  - the `humanizer` skill for text;
  - the `impeccable` skill and `design/DESIGN.md` for agency-grade UI;
  - a list of AI-made patterns to avoid.
- **`find-skills`**, with vetting rules and "one skill per job".
- **Rules 16 to 30:**
  - the red-then-green gate;
  - verifying on what production serves;
  - mocked e2e;
  - gated code-editing agents;
  - one job per purpose;
  - measuring before cutting;
  - live checks;
  - the AI company;
  - scoped reviews;
  - a finding seen twice becomes a check;
  - autonomy;
  - writing;
  - design;
  - PRD first;
  - journeys.
- **Rule 7 corrected:** Next's type check stalled deploys, so `tsc` in CI is the gate.
- **New PLAYBOOK sections:** Replit platform notes, working with the owner, growth.
- **Housekeeping:**
  - sections renumbered (rule numbers unchanged);
  - CONTRIBUTING rewritten so every kind of change has one home;
  - this changelog added.

## 1.0.0 (27 Nov 2026)

- First version from Cogniscore: rules 1 to 15, the Day 0 and first-week checklists, baselines, the starter prompt, and `template/` (AGENTS.md, head-of-design and cto-reviewer, guard hook, CI, design-system check).
