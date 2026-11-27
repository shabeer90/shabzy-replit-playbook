# Contributing

Any project using this playbook can improve it. The aim is that each change makes the playbook better without creating a second, conflicting version of something already here.

## One home for each kind of change

| Kind of change | Goes in | Not in |
|---|---|---|
| What happened on a project (raw) | `learnings/<project>.md` | PLAYBOOK.md |
| A rule the next project should follow | `PLAYBOOK.md` section 1, as a new number at the end | anywhere else; other files link to the rule |
| A checklist item or baseline | the matching PLAYBOOK section (Day 0, security, CI, SEO and GEO, first week) | the rules |
| A role, the work flow, the roadmap and PRD process, the token budget, the autonomy ladder | `template/ORG.md` | PLAYBOOK.md (which only links to it) |
| What an agent checks | that agent's file in `template/.claude/agents/` | other agents' files |
| A skill | `SKILLS.md` | the agent files, which name the skill but don't describe it |
| Platform behaviour (Replit, GitHub, Claude Code) | PLAYBOOK section 11, or the relevant baseline | rules |
| An enforced check | the hook, CI or script in `template/`, plus one line in the rule it enforces | prose alone |

If a change seems to belong in two places, it belongs in one, and the other links to it.

## Before opening a PR

1. **Search first** (`grep -ri <topic>`). If a rule, agent check or skill already covers it, improve that one instead of adding another.
2. **Check ownership.** Each check has one owning agent (`template/ORG.md`). Adding a check to a second agent is a conflict. Move it, or leave it where it is.
3. **Check skills overlap.** A new skill for a job that already has one must replace it, with the reason, or not be added (`SKILLS.md`).
4. **Keep rule numbers.**
   - Never renumber.
   - A rule that's wrong is rewritten in place, with one line: "Was X until <project> showed Y."
   - A rule that no longer applies is marked **Retired**, with the reason, and kept.
5. **Write it plainly.** Same style as the rest: short sentences, specific, no AI tells (the `humanizer` skill helps).
6. **No secrets, client data or personal details.** This repo is public. Keep security lessons general until they're fixed in the project they came from.
7. **Update `CHANGELOG.md`.** Add a line under the next version.

## The bar for a rule

- **It happened.** A real incident, cost or win. General advice is fine in the checklists, but mark it as general.
- **It says what to do.** "Decide RLS per column on day one", not "be careful with RLS".
- **It's checked by something where possible:** a hook, a CI step or a test. A rule that's only in prose gets forgotten (rule 25).

Platform behaviour you haven't confirmed is marked **(check current docs)**.

## Versions

- **Minor (1.x):** additions that don't change what an existing project must do.
- **Major (2.0):** a change that existing projects should adopt, such as a new required reviewer or a hook behaviour change. Say how to upgrade.

Each project records the version it started from in its `AGENTS.md`, so it knows what to pick up later.
