#!/usr/bin/env python3
"""Validate a multi-tier API rate-limit scheme for internal consistency.

Usage:
    python3 validate_limits.py --tiers "free:60:60,pro:600:60,enterprise:6000:60" --burst 20
"""
import argparse


def parse_tiers(spec):
    tiers = []
    for part in spec.split(","):
        name, reqs, window = part.split(":")
        tiers.append({"name": name, "requests": int(reqs), "window": int(window)})
    return tiers


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiers", required=True, help='e.g. "free:60:60,pro:600:60"')
    ap.add_argument("--burst", type=int, default=0, help="burst allowance (extra requests allowed instantly)")
    args = ap.parse_args()

    tiers = parse_tiers(args.tiers)
    issues = []

    print("Tier analysis:")
    prev_rps = None
    for t in tiers:
        rps = t["requests"] / t["window"]
        print(f"  {t['name']:12s}  {t['requests']:6d} req / {t['window']:4d}s  ->  {rps:.3f} req/s")

        if args.burst > t["requests"]:
            issues.append(f"burst ({args.burst}) exceeds {t['name']}'s entire window budget ({t['requests']}) — the window limit will never actually trigger for this tier")

        if prev_rps is not None and rps < prev_rps:
            issues.append(f"tier '{t['name']}' ({rps:.3f} req/s) is stricter than the previous tier ({prev_rps:.3f} req/s) — tiers should not get stricter as they go up")
        prev_rps = rps

    print()
    if not issues:
        print("No inconsistencies found — tiers scale monotonically and burst fits within every tier's budget.")
    else:
        print(f"{len(issues)} issue(s) found:")
        for i in issues:
            print(f"  - {i}")


if __name__ == "__main__":
    main()
