---
name: loan-amortization-calculator
description: Generate a full loan amortization schedule (payment-by-payment principal/interest breakdown) from principal, rate, and term, with the total-interest-paid figure computed from the real schedule rather than estimated. Use whenever the user wants a mortgage/auto-loan/personal-loan payment schedule, wants to compare loan offers, or asks how much interest they'll pay over the life of a loan.
---

# Loan Amortization Calculator

## Purpose
"Total interest paid" and "payoff timeline under extra payments" are easy to get wrong with quick mental math — the real number comes from summing an actual period-by-period schedule, not a rough principal × rate × years estimate (which ignores that the interest portion shrinks every period as principal is paid down).

## When to use
- User wants a payment schedule for a mortgage, auto loan, student loan, or personal loan.
- User wants to compare total interest across two loan offers (different rate/term combinations).
- User wants to know the effect of extra principal payments on total interest and payoff date.

## Workflow

1. Gather: principal amount, annual interest rate, term length (months or years), payment frequency (usually monthly), and optionally an extra-payment amount per period.

2. Run the calculator:
   ```bash
   python3 scripts/amortize.py --principal 300000 --rate 6.5 --years 30 --extra 200
   ```
   `--extra` is optional (extra principal payment applied each period).

3. The script outputs: the standard monthly payment, total interest paid over the life of the loan, actual payoff time if extra payments are applied (which is usually shorter than the nominal term), and — on request — the full period-by-period schedule.

4. When comparing two loan offers, run both and present the total-interest and payoff-time deltas side by side rather than just the two monthly payment numbers — a lower monthly payment with a longer term can mean much more total interest, which is often the number that actually matters for the decision.

5. This is descriptive math only — present the numbers; don't tell the user which loan to choose or whether to refinance, since that also depends on factors outside these numbers (cash flow needs, opportunity cost of the extra payment, tax treatment). Note Claude isn't a financial advisor if the conversation moves toward a recommendation.

## Notes
- Assumes standard fixed-rate, fully-amortizing monthly payments (the overwhelmingly common case for mortgages/auto loans). Flag if the user's loan has a different structure (ARM, interest-only period, balloon payment) since the standard formula doesn't apply as-is.
- Rounding: real lenders round each period's payment to the cent, which the script does too, since summed rounding error against an unrounded calculation can shift the final "total interest" figure slightly.
