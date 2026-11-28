---
name: lane
description: Decide how much process a change needs. Use at the start of every piece of work (a bug, a tweak, a feature, anything you or the owner suggests), again before opening its PR, and whenever a change grows or starts touching money, stored data, sign-in, emails, URLs or public claims.
---

# Pick the lane

Process follows the door, not the size. A two-way door can be walked back through: undo it and nobody is hurt. A one-way door can't, so it gets the slow, careful path. Everything else should move fast.

## 1. Is it a one-way door?

It is if any of these is true:

1. It moves or charges money, or changes prices, billing, refunds or payouts.
2. It sends something that can't be recalled: email, SMS, push, a partner webhook, a social post.
3. It deletes or overwrites stored data: destructive migrations, backfills, purge jobs.
4. It touches sign-in, permissions, secrets or personal data, including what gets logged.
5. It publishes a claim that gets indexed or screenshotted (health, legal, price or comparison claims, structured data), or changes URLs, redirects or what search engines can crawl.
6. It can't be switched off within five minutes without a deploy, or switching it off leaves users stuck.
7. Nothing would tell you within an hour if it broke.
8. It changes something others depend on: an API shape, an export format, URLs others link to.

Unsure? It's one-way. `config/lanes.json` lists the paths that make a change one-way in this project, and CI treats any PR touching one as a Bet, whatever its description says.

## 2. The lane

| | Fix | Feature | Bet |
|---|---|---|---|
| Door | two-way | two-way | one-way |
| Size | up to `fix_max_lines` added lines in `config/lanes.json` (deletions are free) | any, but split big PRs | any, but split big PRs |
| Before building | nothing | the top half of `docs/prd/_template.md`, approved by the owner, under **Now** | the whole PRD, including **Undo** and **How we'd notice**, reviewed in PRD mode (`review` skill), approved by the owner, under **Now** |
| Review | CI, and the owner reads the PR | CI, one review with the lenses its paths wake (`review` skill), and QA if it touches the app | as Feature, and the security and data lenses never retire |
| Release | `release` skill | `release` skill | `release` skill, behind a switch where there can be one, and watched for the first hour |

A change can move up a lane, never down. A Fix that grows past the limit is a Feature. A Feature that trips a door is a Bet: stop building and tell the owner, because a Bet needs its PRD first.

**Appetite.** A PRD says how much time the work is worth. If it isn't done by then, stop and ask the owner to cut scope or re-pitch. Don't quietly carry on.

**Spikes.** A branch that will never be merged, to try something out, needs no lane or PRD. To keep the result, rebuild it as a Feature.

## 3. Read only what the change triggers

From the playbook (https://github.com/shabeer90/shabzy-replit-playbook):
- a database, sign-in, admin or payments: `modules/database.md`;
- public pages, URLs, metadata or the sitemap: `modules/public-site.md`;
- Replit doing something the code doesn't explain: `modules/replit-platform.md`;
- a bug: write the test that fails first (rule 16), then fix it;
- third-party or model text reaching a page: rule 5.

Don't read the whole playbook for a change that triggers none of these.

## 4. The PR header

Every PR description starts with these four lines. CI (`scripts/check_lane.py`) fails the PR without them, or when they don't fit what it changes.

```
Lane: fix | feature | bet
Door: two-way | one-way (which of the eight)
Blast radius: <who or what breaks if this is wrong, and how you'd notice>
PRD: fix | docs/prd/<file>.md
```

Then say what changed, what you ran, what you didn't check, and what the owner must do.
