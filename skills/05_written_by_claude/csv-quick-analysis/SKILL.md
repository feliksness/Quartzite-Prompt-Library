---
name: csv-quick-analysis
description: Fast, dependency-light profiling of a CSV or TSV file — column types, null counts, min/max/mean, top values, and duplicate rows — before doing any deeper analysis. Use whenever the user hands over a CSV/TSV and wants a quick summary, sanity check, or "what's in this file" overview rather than a full report or chart.
---

# CSV Quick Analysis

## Purpose
Give a fast profile of a tabular file so you (or the user) know what you're working with, before writing pandas code, building charts, or importing into a database.

## When to use
- User uploads a CSV/TSV and asks "what's in here" / "summarize this data" / "sanity check this file".
- Before deeper analysis, to catch bad rows, wrong types, or missing data early.
- Not for: full statistical reports, chart generation, or multi-file joins — use the data-analysis skill for those.

## Workflow

1. Run the profiler on the file:
   ```bash
   python3 scripts/profile_csv.py /path/to/file.csv
   ```
2. The script prints, per column: inferred type (int/float/string/date/bool), number of nulls/blanks, number of distinct values, and — for numeric columns — min/max/mean; for string columns — the top 5 most frequent values.
3. It also reports total row count and exact duplicate row count.
4. Read the output and summarize it in plain language for the user: flag columns with unexpectedly high null rates, single-value columns (likely useless), or a duplicate-row count above 0.
5. Only move to deeper analysis (pandas, plotting) once the user confirms the shape of the data looks right, or asks for it directly.

## Notes
- The script uses only the standard library (`csv`, no pandas) so it works even without extra packages installed.
- For files over ~200MB, the script samples the first 200,000 rows rather than reading the whole file, and says so in its output.
