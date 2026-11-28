---
name: release
description: Publish merged work on Replit and check the live site. Use after a PR is merged to main, when the owner asks to publish or redeploy, and when the live-drift check fails.
---

# Release

Replit publishes whatever is in the workspace, not what's on GitHub. A merged PR isn't live until someone pulls `main` into the workspace and publishes, and anything uncommitted in the workspace goes live with it. The owner presses Publish, or approves it.

## Steps

1. **Only from `main`, after the merge.** In the Replit Shell:
   ```bash
   git checkout main && git pull origin main && git status --short
   ```
   Run `pnpm install` too if the lockfile changed. `git status --short` must print nothing. Anything it lists would be published without review: put it through a PR, or discard it.
2. **Publish or redeploy.** Do it after **any** site code or `next.config` change; ISR pages don't pick up config changes on their own.
3. **Check the live site** with the *Live check* command in `AGENTS.md` (rule 22), then run the journeys in `docs/JOURNEYS.md` against it (rule 30).
   - For static artifacts, check `.replit-artifact/artifact.toml` and `public/_redirects` together, and test a known route and an unknown path over HTTP.
   - If the Replit dev workflow renders client-only pages but the published artifact is prerendered, test hydration in a browser against the built artifact too.
4. **Bets:** for the first hour, watch what the PRD's **How we'd notice** names. If it goes wrong, use the **Undo**, then tell the owner.
5. **Record it.** Move the PRD to **Shipped** in `docs/ROADMAP.md`. After a batch, write the retro from `docs/retro-template.md`.

## When the live-drift check fails

`.github/workflows/live-drift.yml` compares the commit the site reports with `main` every day.

- **Uncommitted changes:** someone, or Replit Agent, published from an edited workspace. Put the changes through a PR, then publish from a clean `main`.
- **Not on main:** the workspace was on a branch when it was published. Check out `main`, pull, publish.
- **Merges not live:** a merge has waited more than a day. Publish, or tell the owner why not.
- **No commit reported:** the build didn't run `scripts/write_version.sh`, or git wasn't available when Replit built it.

## What a rollback doesn't undo

Replit's checkpoint rollback restores code, and the development database only if you tick it. It never restores the production database; that needs the database's own backups or point-in-time restore (Replit docs, checked 27 Nov 2026). Emails sent, cards charged and posts published can't be rolled back at all. That's why they're one-way doors.
