#!/usr/bin/env python3
"""Check a raw SQL migration file for common production-safety hazards.

Usage:
    python3 check_migration.py path/to/migration.sql
"""
import argparse
import re
import sys


def strip_comments(sql):
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    return sql


def check(sql):
    findings = []
    clean = strip_comments(sql)
    upper = clean.upper()
    statements = [s.strip() for s in clean.split(";") if s.strip()]

    for stmt in statements:
        u = stmt.upper()

        if re.search(r"DROP\s+TABLE", u):
            findings.append(("CRITICAL", f"DROP TABLE found — irreversible. Statement: {stmt.strip()[:80]}"))

        if re.search(r"DROP\s+COLUMN", u):
            findings.append(("CRITICAL", f"DROP COLUMN found — irreversible, and risks breaking code still reading it. Statement: {stmt.strip()[:80]}"))

        add_notnull = re.search(r"ADD\s+COLUMN\s+.+?\bNOT\s+NULL\b", u)
        if add_notnull and "DEFAULT" not in u:
            findings.append(("CRITICAL", f"ADD COLUMN ... NOT NULL with no DEFAULT — will fail or lock on a populated table. Statement: {stmt.strip()[:80]}"))

        if re.search(r"RENAME\s+(COLUMN|TABLE)", u):
            findings.append(("WARNING", f"RENAME found — breaks any code still deployed against the old name during a rolling deploy. Statement: {stmt.strip()[:80]}"))

        if re.search(r"CREATE\s+(UNIQUE\s+)?INDEX", u) and "CONCURRENTLY" not in u:
            findings.append(("WARNING", f"CREATE INDEX without CONCURRENTLY (Postgres) — will lock writes on large tables for the duration. Statement: {stmt.strip()[:80]}"))

        if re.search(r"ALTER\s+COLUMN\s+.+?\bTYPE\b", u):
            findings.append(("WARNING", f"ALTER COLUMN ... TYPE — can require a full table rewrite depending on the type change and engine. Statement: {stmt.strip()[:80]}"))

    if statements and not any("DOWN" in s.upper() or "ROLLBACK" in s.upper() for s in statements):
        findings.append(("INFO", "No obvious rollback/down statement found in this file — confirm a rollback plan exists separately."))

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()

    with open(args.path, "r") as f:
        sql = f.read()

    findings = check(sql)
    if not findings:
        print("No issues found by the rule-based checks.")
        return

    order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    for sev, msg in sorted(findings, key=lambda x: order[x[0]]):
        print(f"[{sev}] {msg}")

    n_critical = sum(1 for s, _ in findings if s == "CRITICAL")
    sys.exit(1 if n_critical else 0)


if __name__ == "__main__":
    main()
