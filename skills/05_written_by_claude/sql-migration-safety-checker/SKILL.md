---
name: sql-migration-safety-checker
description: Check a SQL schema migration file for changes that lock tables, break running application code, or are irreversible — before it runs against production. Use whenever the user shares a migration file (Alembic, Rails, Django, Prisma, Flyway, raw SQL) and asks to review it, or before running any ALTER/DROP against a live database.
---

# SQL Migration Safety Checker

## Purpose
Migrations that look fine in isolation can take down production: adding a `NOT NULL` column without a default locks the table on some engines; dropping a column an old app version still reads from breaks mid-deploy; renaming a column instead of add-then-backfill-then-drop leaves no rollback path. This skill checks for the specific patterns that cause these incidents.

## When to use
- User shares a migration file and wants it reviewed before running it.
- User is about to run a schema change against a production or shared database.
- Not for reviewing query logic/business correctness — this is specifically about migration *safety* (locking, reversibility, backward compatibility).

## Workflow

1. Run the checker on the migration's raw SQL (extract it first if it's wrapped in a framework migration file):
   ```bash
   python3 scripts/check_migration.py path/to/migration.sql
   ```

2. It flags:
   - **CRITICAL**: `DROP TABLE`/`DROP COLUMN` with no corresponding backup/rename step — irreversible data loss risk
   - **CRITICAL**: `ALTER TABLE ... ADD COLUMN ... NOT NULL` with no `DEFAULT` — locks/fails on populated tables in most engines
   - **WARNING**: `RENAME COLUMN`/`RENAME TABLE` — breaks any code still deployed against the old name during a rolling deploy; prefer add-new/backfill/drop-old across multiple deploys
   - **WARNING**: adding an index without `CONCURRENTLY` (Postgres) or equivalent online option — locks writes for the duration on large tables
   - **INFO**: missing a corresponding "down"/rollback migration

3. Walk through flags in severity order with the user. For CRITICAL items on a migration about to run against production, treat it as a hard stop until the user confirms it's intentional and has a rollback plan.

4. Suggest the safer multi-step pattern where relevant (e.g., "add nullable column → backfill in batches → add NOT NULL constraint separately → deploy code that uses it → only then drop the old column in a later migration").

## Notes
- Pattern-based, not a full SQL parser — always still recommend a staging-environment dry run for anything non-trivial, especially on large tables.
- Engine-specific locking behavior differs (Postgres/MySQL/SQL Server); when unsure which engine, ask, since the same statement can be instant on one and lock for minutes on another.
