#!/usr/bin/env python3
"""Compute standard financial ratios from whatever balance-sheet/income-statement
figures are actually provided, explicitly reporting any ratio it can't compute.

Usage:
    python3 calc_ratios.py --input figures.json
"""
import argparse
import json


# Each ratio: (name, required_keys, compute_fn)
def define_ratios():
    return [
        ("Current Ratio", ["current_assets", "current_liabilities"],
         lambda f: f["current_assets"] / f["current_liabilities"]),

        ("Quick Ratio", ["current_assets", "inventory", "current_liabilities"],
         lambda f: (f["current_assets"] - f["inventory"]) / f["current_liabilities"]),

        ("Cash Ratio", ["cash", "current_liabilities"],
         lambda f: f["cash"] / f["current_liabilities"]),

        ("Debt-to-Equity", ["total_liabilities", "total_equity"],
         lambda f: f["total_liabilities"] / f["total_equity"]),

        ("Debt Ratio", ["total_liabilities", "total_assets"],
         lambda f: f["total_liabilities"] / f["total_assets"]),

        ("Equity Multiplier", ["total_assets", "total_equity"],
         lambda f: f["total_assets"] / f["total_equity"]),

        ("Gross Margin", ["revenue", "cogs"],
         lambda f: (f["revenue"] - f["cogs"]) / f["revenue"]),

        ("Net Margin", ["net_income", "revenue"],
         lambda f: f["net_income"] / f["revenue"]),

        ("Operating Margin", ["operating_income", "revenue"],
         lambda f: f["operating_income"] / f["revenue"]),

        ("Return on Assets (ROA)", ["net_income", "total_assets"],
         lambda f: f["net_income"] / f["total_assets"]),

        ("Return on Equity (ROE)", ["net_income", "total_equity"],
         lambda f: f["net_income"] / f["total_equity"]),

        ("Asset Turnover", ["revenue", "total_assets"],
         lambda f: f["revenue"] / f["total_assets"]),

        ("Interest Coverage", ["operating_income", "interest_expense"],
         lambda f: f["operating_income"] / f["interest_expense"]),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="path to a JSON file of known figures")
    args = ap.parse_args()

    with open(args.input) as f:
        figures = json.load(f)

    ratios = define_ratios()
    computed = []
    skipped = []

    for name, required, fn in ratios:
        missing = [k for k in required if k not in figures]
        if missing:
            skipped.append((name, missing))
            continue
        try:
            value = fn(figures)
            computed.append((name, value))
        except ZeroDivisionError:
            skipped.append((name, ["division by zero in a required input"]))

    print("Computed ratios:")
    for name, value in computed:
        if "Margin" in name or "ROA" in name or "ROE" in name:
            print(f"  {name:28s} {value*100:8.2f}%")
        else:
            print(f"  {name:28s} {value:8.3f}")

    if skipped:
        print("\nNot computable (missing inputs):")
        for name, missing in skipped:
            print(f"  {name:28s} missing: {', '.join(missing)}")


if __name__ == "__main__":
    main()
