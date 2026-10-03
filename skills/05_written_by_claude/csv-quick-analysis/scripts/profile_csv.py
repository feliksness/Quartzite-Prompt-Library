#!/usr/bin/env python3
"""Dependency-free quick profiler for CSV/TSV files.

Usage:
    python3 profile_csv.py path/to/file.csv [--delimiter ,]
"""
import argparse
import csv
import sys
from collections import Counter
from datetime import datetime

MAX_ROWS = 200_000


def sniff_delimiter(sample: str, forced: str | None) -> str:
    if forced:
        return forced
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;|").delimiter
    except csv.Error:
        return ","


def try_type(value: str):
    if value == "" or value is None:
        return None
    v = value.strip()
    for parser, tname in (
        (int, "int"),
        (float, "float"),
    ):
        try:
            parser(v)
            return tname
        except ValueError:
            pass
    if v.lower() in ("true", "false"):
        return "bool"
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            datetime.strptime(v, fmt)
            return "date"
        except ValueError:
            pass
    return "string"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--delimiter", default=None)
    args = ap.parse_args()

    with open(args.path, "r", newline="", encoding="utf-8-sig", errors="replace") as f:
        sample = f.read(4096)
        f.seek(0)
        delim = sniff_delimiter(sample, args.delimiter)
        reader = csv.DictReader(f, delimiter=delim)
        columns = reader.fieldnames or []

        col_values = {c: [] for c in columns}
        row_hashes = Counter()
        total_rows = 0
        truncated = False

        for row in reader:
            total_rows += 1
            if total_rows > MAX_ROWS:
                truncated = True
                break
            row_hashes[tuple(row.items())] += 1
            for c in columns:
                col_values[c].append(row.get(c, ""))

    print(f"File: {args.path}")
    print(f"Delimiter detected: {delim!r}")
    print(f"Rows analyzed: {total_rows}{' (truncated at ' + str(MAX_ROWS) + ')' if truncated else ''}")
    dup_rows = sum(c - 1 for c in row_hashes.values() if c > 1)
    print(f"Exact duplicate rows: {dup_rows}")
    print(f"Columns: {len(columns)}")
    print()

    for c in columns:
        vals = col_values[c]
        n = len(vals)
        nulls = sum(1 for v in vals if v is None or v.strip() == "")
        non_null = [v for v in vals if v is not None and v.strip() != ""]
        distinct = len(set(non_null))

        types = Counter(try_type(v) for v in non_null)
        inferred = types.most_common(1)[0][0] if types else "empty"

        print(f"- {c}  [{inferred}]  nulls={nulls}/{n}  distinct={distinct}")

        if inferred in ("int", "float") and non_null:
            nums = []
            for v in non_null:
                try:
                    nums.append(float(v))
                except ValueError:
                    pass
            if nums:
                print(f"    min={min(nums):.4g}  max={max(nums):.4g}  mean={sum(nums)/len(nums):.4g}")
        elif non_null:
            top = Counter(non_null).most_common(5)
            top_str = ", ".join(f"{v!r}={cnt}" for v, cnt in top)
            print(f"    top values: {top_str}")


if __name__ == "__main__":
    main()
