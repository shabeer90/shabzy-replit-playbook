# Changelog

## 2.0.0 (27 Nov 2026)

- Four further approved Ihsan lessons: distinguish Replit-provided guidance from installed skills in `SKILLS.md`; record actual review methods and bounded specialist handoffs in `template/ORG.md`; separate implementation, privacy and live-release evidence in the QA report. Raw entries extend `learnings/ihsan.md`.
- **Upgrade for these additions:** use the provider/availability notes when choosing tools, and copy the handoff/review-record guidance and expanded QA report into existing projects. No new roles, numbered rules, installed skills, hooks or CI behaviour.
- Eight approved Ihsan lessons: production-bundle checks (rule 17), controlled non-production integration tests (rule 18), preview proxy QA, cached private-screen access, private crawler controls, resolved dependency verification, private error logging and accurate metric labels. Raw evidence summaries are in `learnings/ihsan.md`.
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
