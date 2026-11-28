---
name: review
description: Independent review of a Feature or Bet branch before it's merged, and of a Bet's PRD before it's built. Use when a branch is ready for review or a PRD needs its review lines. Never use it on work you built yourself.
---

# Review

You didn't build this. Assume it has a bug until you've looked. There is one review, with lenses chosen by what the change touches, not a panel of reviewers.

**Who runs it.** Claude Code's `reviewer` agent, or, without Claude Code, a new Replit Agent chat that didn't build the change. The second is weaker (same model, same blind spots), so say which it was. With neither, the owner reads the diff with this file open.

## 1. Read the change

- The PR header (`lane` skill) and the PRD it links.
- `git diff origin/main...HEAD`, then every changed function in full, not just the hunk.

## 2. Every review checks

- **Delivery:** it does everything the PRD (or the Fix line) asked, and nothing more. Anything extra is a finding, and the idea goes under **Parked ideas** in `docs/ROADMAP.md`.
- **Lane:** the lane and door are right. A one-way door in a two-way lane is a `rethink`.
- **Correctness:** wrong conditions, missing awaits, null cases, off-by-one, swallowed errors. Grep the callers of every changed function and check none breaks.
- **The project's Never list** in `AGENTS.md`: live writes, published facts without evidence, the blocked scripts.
- **Size:** is there a smaller change that fully works? Code nobody asked for, a dependency for a few lines, an abstraction with one caller.
- **Tests:** a bug fix has a test that fails without it, and new logic has a test. Run the suite.
- **Handover:** the PR says what changed, what was run, what wasn't checked, and what the owner must do (pull in Replit, publish, run SQL, set a secret).

Useful skills, where installed: `/code-review` in Claude Code for a bug pass, `codebase-design` for module and interface questions, `next-best-practices` on Next.js.

## 3. Lenses

`lenses.txt` maps each lens to paths. Open `lenses/<lens>.md` for each lens whose paths the diff touches, and only those. On a Bet, also open security and data whenever its door involves them, whatever the paths say.

**Retiring a lens.** Each retro counts, per lens, the runs and the findings. A lens with no findings in 10 runs is commented out in `lenses.txt`, with the date, once the owner agrees. If its risk can be caught by a test or CI step, add that first. Security and data are never retired for Bets.

## PRD mode (Bets only)

Read only the PRD and the code it would touch. For each lens the Bet trips, write one line in the PRD's **Review** section: `<lens>: approve`, or `<lens>: changes needed:` with what and why. Check that **Undo** and **How we'd notice** would actually work.

## Report

Write `.reviews/<branch>.md` (replace `/` with `-` in the branch name). The four header lines from the `lane` skill go first, then:

```
## Review
Revision: <commit>   Done by: <agent, tools used; confirm you didn't build it>
Lenses: <the ones opened, and why>
Not checked: <what, and why>

- [lens] file:line: what breaks, for which input. Fix: <smallest fix>. Verified | Inferred

Owner decisions: <findings for the owner to decide, not blockers>
REVIEW: ship | fix first | rethink
```

If it's clean, say so in one line. On a PR that's already open, paste the file into it as a comment.
