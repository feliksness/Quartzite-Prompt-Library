---
name: financial-ratio-calculator
description: Compute standard financial ratios (liquidity, profitability, leverage, efficiency) from actual balance sheet and income statement figures the user provides, and flag which ratios can't be computed from missing inputs — instead of estimating numbers that weren't given. Use whenever the user shares financial statement figures and wants ratio analysis, a company's financial health assessed, or is comparing two companies' fundamentals.
---

# Financial Ratio Calculator

## Purpose
Ratio analysis is only as good as the inputs — silently guessing a missing "total liabilities" figure to compute a debt ratio produces a number that looks precise but isn't real. This skill computes ratios strictly from the figures given and clearly reports which ratios it could NOT compute due to missing inputs.

## When to use
- User provides balance sheet/income statement line items and wants ratios calculated.
- User wants to compare financial health across two periods or two companies with the same figures.
- Not for stock price prediction, valuation opinions, or "should I invest" advice — present the numbers; note this isn't financial advice for anything beyond descriptive ratio analysis.

## Workflow

1. Collect available inputs. Common ones: current assets, current liabilities, inventory, cash, total assets, total liabilities, total equity, revenue, COGS, net income, operating income, interest expense, total debt.

2. Run the calculator:
   ```bash
   python3 scripts/calc_ratios.py --input figures.json
   ```
   where `figures.json` has whatever line items are known, e.g.:
   ```json
   {"current_assets": 500000, "current_liabilities": 250000, "inventory": 120000,
    "total_liabilities": 800000, "total_equity": 600000, "revenue": 2000000,
    "cogs": 1200000, "net_income": 150000, "total_assets": 1400000}
   ```

3. The script computes every ratio for which it has the required inputs (current ratio, quick ratio, debt-to-equity, gross margin, net margin, ROA, ROE, asset turnover, etc.) and explicitly lists any ratio it skipped along with which input was missing.

4. Present the computed ratios plainly, and note industry context matters — a "good" current ratio differs by sector; don't apply a universal good/bad label without that context, or without the user supplying a benchmark to compare against.

5. If comparing two periods/companies, compute both sets and show the delta, not just two separate tables.

## Notes
- This is descriptive math, not investment advice — present figures and ratios; leave conclusions about buy/sell/invest decisions to the user, and note Claude isn't a financial advisor if the conversation moves in that direction.
- Never silently substitute an industry average or estimate for a genuinely missing input — report it as "not computable: missing X" instead.
