# Adding what a project learned

Any project using this playbook can add to it. Two steps:

1. **Write it down raw** in `learnings/<project>.md`: the date, what happened, what it cost, and what fixed it. Add it the same day; details fade.
2. **Promote it** when it would change what the next project does. Add it to `PLAYBOOK.md` as a rule, with "*On <project>:*" and one line on what happened. If the fix is a file, put it in `template/`.

## The bar for a rule

- **It happened.** A real incident, cost or win, not a best practice copied from a blog. General advice is fine in the checklists, but mark it as general.
- **It says what to do.** "Decide RLS per column on day one", not "be careful with RLS".
- **It's checked by something where possible:** a hook, a CI step or a test. A rule only in prose gets forgotten.
- **No secrets, client data or personal details.** This repo is public.

Platform behaviour you haven't confirmed (Replit, Supabase, GitHub) is marked **(check current docs)**.

## Changing a rule

When a later project shows that a rule is wrong, change it and keep one line of history: "Was X until <project> showed Y."
