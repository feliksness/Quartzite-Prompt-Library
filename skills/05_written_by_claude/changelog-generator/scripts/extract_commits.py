#!/usr/bin/env python3
"""Extract git commits in a range as JSON lines, for changelog generation.

Usage:
    python3 extract_commits.py --range "v1.2.0..HEAD" --repo /path/to/repo
    python3 extract_commits.py --since "2 weeks ago" --repo /path/to/repo
"""
import argparse
import json
import subprocess
import sys


SEP = "\x1f"  # unit separator, unlikely to appear in commit text
FIELDS = ["H", "an", "ad", "s", "b"]  # hash, author name, date, subject, body


def run_git_log(repo: str, rng: str | None, since: str | None):
    fmt = SEP.join(f"%{f}" for f in FIELDS) + "\x1e"  # record separator at end
    cmd = ["git", "-C", repo, "log", f"--pretty=format:{fmt}", "--date=short"]
    if rng:
        cmd.append(rng)
    if since:
        cmd.append(f"--since={since}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"git log failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def parse_records(raw: str):
    records = [r for r in raw.split("\x1e") if r.strip()]
    for rec in records:
        parts = rec.strip("\n").split(SEP)
        if len(parts) < 5:
            continue
        h, an, ad, s, b = parts[0], parts[1], parts[2], parts[3], parts[4]
        yield {
            "hash": h.strip(),
            "author": an.strip(),
            "date": ad.strip(),
            "subject": s.strip(),
            "body": b.strip(),
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--range", dest="rng", default=None, help='e.g. "v1.2.0..HEAD"')
    ap.add_argument("--since", default=None, help='e.g. "2 weeks ago"')
    args = ap.parse_args()

    if not args.rng and not args.since:
        args.since = "1 month ago"

    raw = run_git_log(args.repo, args.rng, args.since)
    count = 0
    for commit in parse_records(raw):
        print(json.dumps(commit))
        count += 1

    if count == 0:
        print("(no commits found in range)", file=sys.stderr)


if __name__ == "__main__":
    main()
