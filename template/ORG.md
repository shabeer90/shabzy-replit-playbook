# How this AI company is organised

Every project runs as a small AI company. The owner is the board. Agents hold the jobs, and **each job has exactly one owner**, so two agents never do the same work and spend tokens twice.

## The roles

| Role | Who | Owns | Doesn't do |
|---|---|---|---|
| **Board** | the owner (a human) | Strategy, approving PRDs, what goes under Now on the roadmap, anything that goes live, merging, money, secrets, the autonomy level | Day-to-day building |
| **CEO** | the main agent session | The plan, delegating to the right role, running PRD reviews, the token budget, reporting to the owner, retros and playbook contributions | Writing PRDs, reviewing its own work |
| **CPO** | `cpo` agent | What gets built and why: PRDs, the leadership review of each PRD, `docs/ROADMAP.md`, `docs/JOURNEYS.md`, parking every unplanned idea | How it's built |
| ↳ Head of Design | `head-of-design` | `design/DESIGN.md`, tokens, `components/ui/`; making it look agency-built, not AI-made; DESIGN review | Copy, code quality |
| **CTO** | `cto-reviewer` | How the code is built: correctness, callers, size, tests | Security depth, delivery against the PRD |
| ↳ Engineering manager | `em-reviewer` | Delivery: built what the PRD asked, nothing extra, the journeys still work end to end, clean handover | Whether the PRD was right |
| ↳ QA | `qa-tester` | Every journey in `docs/JOURNEYS.md` end to end, plus the new feature like a user; e2e tests | Code review |
| ↳ Security | `security-reviewer` | Trust-boundary failures | General code style |
| ↳ Head of Data | `head-of-data` | Schema, access rules, migrations, live writes, data quality (projects with a database) | UI |
| **CMO** | `cmo-reviewer` | Every word a customer reads (no AI slop), claims, SEO and GEO on public sites; growth plans | Code, visuals |

The builder is whichever agent writes the code, usually the CEO session or a subagent it starts. It never reviews its own work.

## No feature factory

It's easy, especially on Replit, to keep building whatever gets suggested next. The product ends up with lots of half-finished features, and nobody knows what it's for. Three files stop that:

- **`docs/ROADMAP.md`** is the only list of what we build. **Now** holds three items at most. Every other idea, whoever suggested it (the owner in passing, Replit Agent, another agent, a user), goes under **Parked ideas** with its source and the date.
- **`docs/prd/`:** nothing bigger than a small fix is built without an approved PRD. The guard hook won't open a PR without a `PRD:` line linking one with `Status: approved`, or `PRD: fix`.
- **`docs/JOURNEYS.md`** lists the user journeys that must always work end to end. Every feature is judged by whether the user can still get from start to done, not by whether the new piece works on its own.

## How a piece of work moves

1. **The owner asks.** The CEO checks the roadmap.
   - **Not under Now:** the idea is parked, or the owner chooses to move it up.
   - **Small fix** (a bug, a copy tweak, a dependency bump): skips the PRD.
2. **PRD.** The CPO writes it from `docs/prd/_template.md`, including the user journey.
3. **Leadership review of the PRD.** The CEO runs the agents whose area it touches in PRD-review mode (CTO always; CMO, security, data and design as relevant). Each writes one line in the PRD. Problems are fixed here, where they're cheapest.
4. **The owner approves** the PRD, and it moves to **Now**.
5. **Before building:**
   - head-of-design adds any missing component;
   - head-of-data designs any schema change.
6. **Build** test-first (`tdd`), with ponytail. Only what the PRD says. A good idea that comes up while building gets parked, not built.
7. **Review the build.** Every reviewer in `.claude/reviewers.txt` whose paths the change touches reviews it, in parallel, and writes to `.reviews/<branch>.md`, which also carries the `PRD:` line.
   - **QA** runs every journey end to end, not only the new feature.
   - **EM** checks the build against the PRD and confirms the journeys passed.
8. **Fix and re-run.** The builder fixes confirmed findings, and only the reviewer that raised each one re-runs.
9. **Open the PR.** The hook allows `gh pr create` once the PRD is approved and every required reviewer says `ship`. The review file goes in the PR, and Auto-fix is turned on.
10. **Ship.** The owner merges, pulls in Replit and publishes. The CEO runs the live check and the journeys against the live site, then moves the PRD to **Shipped**.
11. **Learn.** After each batch, the CEO writes a retro, and anything reusable goes to the playbook.

## Token budget

Reviews are where the tokens go, so they're scoped:

- **Path-scoped reviewers.** `.claude/reviewers.txt` gives each reviewer the paths it cares about. A docs-only change wakes only the EM; a copy change doesn't wake the data reviewer.
- **One-line sign-off when out of scope.** A reviewer whose area isn't touched in substance says so and stops.
- **Reviewers read the diff and the functions it touches,** not the whole repo.
- **Model per role,** set in each agent's `model:` frontmatter (check current Claude Code docs for the allowed values):
  - the strongest model for CTO, security, data and CPO, where a miss is expensive;
  - a cheaper one for EM, QA, design and CMO.
- **No double work:** each check has one owner (the table above). If two agents' instructions overlap, fix the instructions; don't run both.
- **Expensive skills by decision only:** the full `security-audit`, a full site crawl (`audit-website`), a full `impeccable` critique of every page. These run at launch and at milestones, with the owner choosing the depth.
- **Measure it:**
  - The CEO notes agents run and rough token use per batch in the retro.
  - Usage per feature should fall over time.
  - If it doesn't, the retro says which review cost the most and whether it found anything.

## Getting better and more autonomous

- **A finding seen twice becomes a check.** The CEO turns it into a test, a hook rule or a CI step, so no reviewer has to spot it a third time. This is how review cost falls and autonomy rises.
- **Every batch ends with a retro** (`docs/retro-template.md`). Lessons that apply beyond this project go to the playbook's `learnings/<project>.md`, and become rules there when they'd change what the next project does.
- **The autonomy ladder.** The owner moves the project up a level, never an agent, and records it in `AGENTS.md`.

| Level | Agents may, without asking | Earned by |
|---|---|---|
| 0: Setup | Research, draft, open PRs | Default |
| 1: Trusted builder | Build features from an approved PRD; fix CI and review comments on their own PRs | A clean first release |
| 2: Trusted shipper | Merge PRs that touch only docs, copy or tests, once every reviewer says ship | Several batches with no incident traced to a review miss |
| 3: Operator | Run approved, scripted live jobs on a schedule (reports, checks), never live data writes | The owner's explicit decision, per job |

Never delegated, at any level: secrets, live data writes outside an approved script, merging code changes to `main`, spending money, posting publicly as the owner.
