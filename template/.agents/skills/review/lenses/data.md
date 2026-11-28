# Data lens

Schema, queries, data jobs and stored data. head-of-data owns how they're designed; this lens checks a change against that. On a Bet that writes or deletes stored data or touches personal data, this lens always runs and is never retired.

If the diff touches no schema, query, data job or stored data, say so in one line and close the lens.

## Check

- **Access rules:** a new table or column without RLS or grants; the service role used on a public path.
- **Query correctness:**
  - filters and joins that silently drop rows;
  - N+1 queries;
  - missing indexes for new filters;
  - unbounded selects.
- **Write paths:** idempotent, they don't overwrite better data with worse (oldest-wins, empty scrapes), and they have guards.
- **Migrations:** additive first, backfills in batches, a written rollback, and any live run written as an owner step, never run by an agent.
- **Data quality:**
  - values parsed from third-party text are validated;
  - units and currencies are explicit;
  - nulls are handled.
- **Privacy:**
  - personal data is minimised;
  - consent is recorded where needed.

Use the `supabase-postgres-best-practices` skill for Postgres or Supabase.

## In the report

For each issue: file:line, what goes wrong with which data, the fix, and **Verified** or **Inferred**.
