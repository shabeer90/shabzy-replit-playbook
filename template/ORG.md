# How this AI company is organised

Every project runs as a small AI company. The owner is the board. Agents hold the jobs, and **each job has exactly one owner**, so two agents never do the same work and spend tokens twice.

Most changes never meet most of the company. A Fix involves the builder, CI and the owner. Specialists wake only for the changes that need them: the lane, and the paths in `.agents/skills/review/lenses.txt`, decide which.

## The roles

| Role | Who | Owns | Wakes up for |
|---|---|---|---|
| **Board** | the owner (a human) | Strategy, approving PRDs, what goes under Now, anything that goes live, merging, money, secrets, the stage and the autonomy level | Every PR (reading it), every PRD, every release |
| **CEO** | the main agent session | Picking the lane, delegating, the token budget, reporting to the owner, retros and playbook contributions | Every change |
| **Builder** | usually Replit Agent (`replit.md`), sometimes the CEO or a subagent | Writing the code, test-first, the smallest complete change | Every change; never reviews its own work |
| **CPO** | `cpo` agent | PRDs, `docs/ROADMAP.md`, `docs/JOURNEYS.md`, parking unplanned ideas | Features and Bets |
| **Head of Design** | `head-of-design` | `design/DESIGN.md`, tokens, `components/ui/` | A change that needs a new component; DESIGN.md before launch |
| **Head of Data** | `head-of-data` | Schema, access rules, migrations, live-write steps (projects with a database) | A schema or data change, before it's built |
| **Reviewer** | `reviewer` agent, following the `review` skill | One independent review, with the security, data, design and words lenses that the paths wake | Features and Bets; a Bet's PRD |
| **QA** | `qa-tester` | Every journey end to end, the new feature like a user, e2e tests | Features and Bets that touch the app |

## Stages

`AGENTS.md` records the stage. The owner moves it.

- **Exploring:** no real users yet. Do the Day 0 list and nothing more of the setup. Spikes (branches that are never merged) are fine. Write a journey's test once the journey exists. `DESIGN.md`, the live check and the rest of the before-launch list wait.
- **Launched:** real people use it. The before-launch list is done, journeys and the live check are required, and the drift check runs daily.

Lanes apply in both stages. A Bet is a Bet even with no users, because secrets, money and sent emails don't care whether you've launched.

## No feature factory

It's easy, especially on Replit, to keep building whatever gets suggested next. The product ends up with lots of half-finished features, and nobody knows what it's for. Three files stop that:

- **`docs/ROADMAP.md`** is the only list of what we build. **Now** holds three Features or Bets at most. **Next** holds what the owner has agreed to do after them, still without a PRD. Every other idea, whoever suggested it (the owner in passing, Replit Agent, another agent, a user), goes under **Parked ideas** with its source and the date.
- **`docs/prd/`:** no Feature or Bet is built without an approved PRD. CI (`scripts/check_lane.py`) fails a PR that says Feature or Bet without a `PRD:` line linking one with `Status: approved`.
- **`docs/JOURNEYS.md`** lists the user journeys that must always work end to end. Every feature is judged by whether the user can still get from start to done, not by whether the new piece works on its own.

## How a piece of work moves

The `lane` skill (`.agents/skills/lane/SKILL.md`) is the source for each lane's steps. In short:

- **Fix:** build it, CI passes, the owner reads the PR and merges (at autonomy level 2, an agent merges once CI passes), then the `release` skill.
- **Feature:** a one-page PRD under **Now**, approved by the owner. head-of-design and head-of-data go first if it needs something new from them. Build test-first. One review, and QA if it touches the app. The owner merges, then the `release` skill.
- **Bet:** a full PRD with **Undo** and **How we'd notice**, reviewed in PRD mode before the owner approves it. Then as a Feature, released behind a switch where there can be one, and watched for the first hour.

A good idea that comes up while building is parked, not built. After each batch, the CEO writes a retro, and anything reusable goes to the playbook.

## Handing work to another agent

When the CEO hands a job to another agent, the handoff says:
- **The goal:** a link to the approved PRD (or the Fix) and its acceptance checks.
- **Decisions already made:** a link to where they're recorded. Say which earlier ideas were replaced, and don't copy the decisions into the handoff.
- **What it touches:** routes, files, callers and interfaces, and what mustn't break.
- **Data and privacy:** what data the agent may use, which test accounts, and what it must clean up.
- **What the agent may do:** advise, review or build. A review isn't permission to edit, change data or publish.
- **What to hand back:** the output, the evidence, and what it couldn't check. Each check has one owner, so link another agent's result instead of repeating it.

## Review records

The review and QA sections in `.reviews/<branch>.md` each say, next to the verdict:
- what it actually did (read the code, ran tests, used a browser);
- on which revision and environment;
- that it didn't build the change itself;
- what it couldn't check.

A reviewer's title isn't proof a review happened. If the right tool wasn't available, say what was used instead and what that left uncovered. A general agent reading the code isn't an architecture review, and running Playwright by hand isn't the specialised browser tool. Never mark the builder's own checks as independent.

QA owns the test report. The security lens owns privacy findings; QA can pass it observations but doesn't give a security verdict. The CEO's checks on the live site after release stay separate from QA before the PR.

## Token budget

Reviews are where the tokens go, so they follow the lane:

- **Fixes get no review agents.** CI and the owner's read cover a small, reversible change.
- **One reviewer, not a panel.** A lens is a checklist the reviewer opens, not another agent reading the same diff. `.agents/skills/review/lenses.txt` says which paths wake which lens.
- **Retire what finds nothing.** The retro counts each lens's runs and findings. A lens with no findings in 10 runs is switched off, with the owner's OK, after any test or CI step that can catch its risk is in place. Security and data never retire for Bets.
- **Reviewers read the diff and the functions it touches,** not the whole repo.
- **Model per role,** set in each agent's `model:` frontmatter (**check current docs** for the allowed values): `inherit` (the session's model) for the reviewer and CPO, where a miss is expensive; a cheaper one for QA and design.
- **Expensive skills by decision only:** the full `security-audit`, a full site crawl (`audit-website`), a full `impeccable` critique of every page. These run at launch and at milestones, with the owner choosing the depth.
- **Measure it.** The retro notes agents run and rough token use per batch. Usage per feature should fall over time.

## Getting better and more autonomous

- **A finding seen twice becomes a check.** The CEO turns it into a test or a CI step (a hook rule only binds Claude Code), so no reviewer has to spot it a third time. This is how review cost falls and autonomy rises.
- **Every batch ends with a retro** (`docs/retro-template.md`). Lessons that apply beyond this project go to the playbook's `learnings/<project>.md`, and become PLAYBOOK rules when they'd change what the next project does.
- **The autonomy ladder.** The owner moves the project up a level, never an agent, and records it in `AGENTS.md`.

| Level | Agents may, without asking | Earned by |
|---|---|---|
| 0: Setup | Research, draft, open PRs | Default |
| 1: Trusted builder | Build Features from an approved PRD; fix CI and review comments on their own PRs | A clean first release |
| 2: Trusted shipper | Merge Fixes once CI passes | Several batches with no incident traced to a Fix |
| 3: Operator | Run approved, scripted live jobs on a schedule (reports, checks), never live data writes | The owner's explicit decision, per job |

Never delegated, at any level: secrets, live data writes, merging a Feature or Bet, spending money, posting publicly as the owner.
