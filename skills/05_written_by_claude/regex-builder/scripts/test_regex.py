#!/usr/bin/env python3
"""Verify a regex pattern against positive and negative sample strings.

Usage:
    python3 test_regex.py --pattern '^\\d{3}-\\d{4}$' \
        --match "555-1234" "000-0000" \
        --no-match "abc" "555-12345"
    Optional: --flags i  (any combination of i, m, s, x)
"""
import argparse
import re
import sys

FLAG_MAP = {"i": re.IGNORECASE, "m": re.MULTILINE, "s": re.DOTALL, "x": re.VERBOSE}


def build_flags(flag_str: str | None) -> int:
    flags = 0
    if flag_str:
        for ch in flag_str:
            if ch in FLAG_MAP:
                flags |= FLAG_MAP[ch]
    return flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", required=True)
    ap.add_argument("--flags", default="")
    ap.add_argument("--match", nargs="*", default=[], help="strings that SHOULD match")
    ap.add_argument("--no-match", nargs="*", default=[], help="strings that should NOT match")
    args = ap.parse_args()

    try:
        compiled = re.compile(args.pattern, build_flags(args.flags))
    except re.error as e:
        print(f"PATTERN ERROR: {e}")
        sys.exit(1)

    all_pass = True

    for s in args.match:
        m = compiled.search(s)
        if m:
            groups = m.groups()
            gtxt = f"  groups={groups}" if groups else ""
            print(f"PASS  match      {s!r}{gtxt}")
        else:
            print(f"FAIL  should match but didn't: {s!r}")
            all_pass = False

    for s in getattr(args, "no_match"):
        m = compiled.search(s)
        if not m:
            print(f"PASS  no-match   {s!r}")
        else:
            print(f"FAIL  should NOT match but did: {s!r} -> matched {m.group(0)!r}")
            all_pass = False

    print()
    print("ALL PASS" if all_pass else "SOME FAILED — revise the pattern")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
