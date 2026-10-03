---
name: sql-lint
description: Catch common, costly SQL mistakes — SELECT *, missing WHERE on UPDATE/DELETE, unqualified JOINs, non-sargable predicates — before a query gets run. Use whenever the user shares a SQL query and asks to review it, optimize it, or check it's safe to run, especially against a production database.
---

# SQL Lint & Safety Check

## Purpose
A quick, rule-based pass over a SQL query to flag the mistakes that most often cause outages or slow queries, before worrying about deeper query-plan optimization.

## When to use
- User pastes a query and asks "does this look right" / "is this safe to run" / "why is this slow".
- Before running any UPDATE/DELETE the user drafted, as a safety check.
- Not a substitute for an actual EXPLAIN/EXPLAIN ANALYZE against the real database — recommend that for real performance tuning.

## Workflow

1. Run the linter on the query:
   ```bash
   python3 scripts/lint_sql.py "SELECT * FROM orders WHERE customer_id = 5"
   ```
   or pipe from a file: `python3 scripts/lint_sql.py --file query.sql`

2. The script flags, with severity:
   - **CRITICAL**: `UPDATE`/`DELETE` with no `WHERE` clause (would touch every row)
   - **WARNING**: `SELECT *` (fetches unneeded columns, breaks on schema changes)
   - **WARNING**: leading-wildcard `LIKE '%foo'` (can't use an index)
   - **WARNING**: `JOIN` without an explicit `ON`/`USING` (risk of accidental cross join)
   - **INFO**: function wrapped around an indexed column in `WHERE` (e.g. `WHERE YEAR(created_at) = 2024`) — not sargable, prevents index use
   - **INFO**: `NOT IN` with a subquery (breaks silently if the subquery returns a NULL)

3. Walk through each flag with the user in order of severity — never let a CRITICAL flag pass silently, especially before running a DELETE/UPDATE in production.

4. Suggest the concrete fix for each flag (e.g. rewrite `WHERE YEAR(created_at) = 2024` as `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'`).

## Notes
- This is pattern-based, not a full SQL parser — it won't catch everything, and can occasionally flag something that's actually fine. Use judgment, and treat CRITICAL flags on destructive statements as a hard stop until confirmed intentional.
- Dialect-agnostic by design (works across Postgres/MySQL/SQLite syntax); doesn't check dialect-specific syntax validity.
