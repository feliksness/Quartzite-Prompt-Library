#!/usr/bin/env python3
"""Rule-based SQL safety/quality linter (regex-based, dialect-agnostic).

Usage:
    python3 lint_sql.py "SELECT * FROM t WHERE id = 1"
    python3 lint_sql.py --file query.sql
"""
import argparse
import re
import sys


def strip_comments(sql: str) -> str:
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    return sql


def lint(sql: str):
    findings = []
    clean = strip_comments(sql)
    upper = clean.upper()

    # CRITICAL: UPDATE/DELETE without WHERE
    for stmt in re.finditer(r"\b(UPDATE|DELETE)\b", upper):
        kw = stmt.group(1)
        tail = upper[stmt.end():]
        next_stmt = re.search(r";|\bSELECT\b|\bUPDATE\b|\bDELETE\b|\bINSERT\b", tail)
        scope = tail[:next_stmt.start()] if next_stmt else tail
        if "WHERE" not in scope:
            findings.append(("CRITICAL", f"{kw} statement with no WHERE clause — would affect every row in the table."))

    # WARNING: SELECT *
    if re.search(r"\bSELECT\s+\*", upper):
        findings.append(("WARNING", "SELECT * fetches all columns — list only what you need; breaks silently on schema changes."))

    # WARNING: leading wildcard LIKE
    if re.search(r"\bLIKE\s+'%", clean, re.IGNORECASE):
        findings.append(("WARNING", "LIKE with a leading '%' can't use a standard B-tree index — consider full-text search or a trailing-wildcard rewrite if possible."))

    # WARNING: JOIN without ON/USING
    for m in re.finditer(r"\bJOIN\b", upper):
        tail = upper[m.end():m.end() + 200]
        if "ON" not in tail and "USING" not in tail:
            findings.append(("WARNING", "JOIN found without a nearby ON/USING clause — check this isn't an accidental cross join."))
            break

    # INFO: function wrapped around column in WHERE (non-sargable)
    if re.search(r"WHERE\s+\w+\s*\(\s*\w+\.?\w*\s*\)\s*=", upper):
        findings.append(("INFO", "A function call wraps a column in the WHERE clause — this is usually non-sargable and prevents index use. Rewrite as a range comparison instead if possible."))

    # INFO: NOT IN with subquery
    if re.search(r"NOT\s+IN\s*\(\s*SELECT", upper):
        findings.append(("INFO", "NOT IN (SELECT ...) silently returns no rows if the subquery yields any NULL — consider NOT EXISTS instead."))

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", help="SQL query as a string")
    ap.add_argument("--file", help="path to a .sql file")
    args = ap.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            sql = f.read()
    elif args.query:
        sql = args.query
    else:
        sql = sys.stdin.read()

    findings = lint(sql)
    if not findings:
        print("No issues found by the rule-based checks.")
        return

    order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    for sev, msg in sorted(findings, key=lambda x: order[x[0]]):
        print(f"[{sev}] {msg}")


if __name__ == "__main__":
    main()
