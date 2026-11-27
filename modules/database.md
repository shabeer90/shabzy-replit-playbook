# Database and sign-in

For projects with a database, sign-in, admin or payments. Rules 3, 4, 6 and 10 in [PLAYBOOK.md](../PLAYBOOK.md#the-rules) are the rules; this is the baseline that goes with them. A lite project doesn't need this file until it gets one of those.

## Database (Supabase)

- Write `schema.sql` before the first table exists. Enable RLS on **every** table and write a policy for each role.
- **Anon:** SELECT only, on the columns the page needs (column-level `GRANT`). No INSERT policies unless the feature needs one.
- **Service role:** only server-side, only in jobs and admin routes.
- Check the live state now and then: `select * from pg_policies;` and the column grants. The repo SQL and the live DB drift apart.
- Every table that records an event (clicks, requests) needs a retention rule and an index on the time column.

## Admin and sign-in

Check before launch. A signed session token with an expiry. Rate-limited login. Middleware, plus a check in every route and layout. `SameSite=Strict`, `Secure`, `HttpOnly`. Re-check access when the user returns to the tab, reconnects, and every few minutes while it's open. While that check runs, or if it fails or can't reach the server, hide confidential screens, cancel private requests and clear private caches. Keep unsaved drafts only if the check confirms the same account.
