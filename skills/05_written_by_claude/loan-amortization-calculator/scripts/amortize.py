#!/usr/bin/env python3
"""Generate a real period-by-period loan amortization schedule.

Usage:
    python3 amortize.py --principal 300000 --rate 6.5 --years 30 --extra 200 --show-schedule
"""
import argparse


def monthly_payment(principal, monthly_rate, n_periods):
    if monthly_rate == 0:
        return principal / n_periods
    return principal * (monthly_rate * (1 + monthly_rate) ** n_periods) / ((1 + monthly_rate) ** n_periods - 1)


def build_schedule(principal, annual_rate_pct, years, extra=0.0):
    monthly_rate = (annual_rate_pct / 100) / 12
    n_periods = years * 12
    payment = round(monthly_payment(principal, monthly_rate, n_periods), 2)

    balance = principal
    schedule = []
    period = 0
    total_interest = 0.0

    while balance > 0.005 and period < n_periods * 3:  # safety cap
        period += 1
        interest = round(balance * monthly_rate, 2)
        principal_payment = payment + extra - interest
        if principal_payment > balance:
            principal_payment = balance
            this_payment = principal_payment + interest
        else:
            this_payment = payment + extra
        balance = round(balance - principal_payment, 2)
        total_interest += interest
        schedule.append({
            "period": period,
            "payment": round(this_payment, 2),
            "interest": interest,
            "principal": round(principal_payment, 2),
            "balance": max(balance, 0.0),
        })

    return payment, schedule, round(total_interest, 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--principal", type=float, required=True)
    ap.add_argument("--rate", type=float, required=True, help="annual interest rate, percent, e.g. 6.5")
    ap.add_argument("--years", type=float, required=True)
    ap.add_argument("--extra", type=float, default=0.0, help="extra principal payment per period")
    ap.add_argument("--show-schedule", action="store_true")
    args = ap.parse_args()

    nominal_payment, schedule, total_interest = build_schedule(
        args.principal, args.rate, args.years, args.extra
    )

    nominal_months = int(args.years * 12)
    actual_months = len(schedule)

    print(f"Principal:            ${args.principal:,.2f}")
    print(f"Annual rate:          {args.rate}%")
    print(f"Nominal term:         {args.years} years ({nominal_months} payments)")
    print(f"Standard payment:     ${nominal_payment:,.2f} / month")
    if args.extra:
        print(f"Extra payment:        ${args.extra:,.2f} / month")
    print(f"Actual payoff time:   {actual_months} payments ({actual_months/12:.2f} years)")
    if args.extra and actual_months < nominal_months:
        saved_months = nominal_months - actual_months
        print(f"  -> paid off {saved_months} months ({saved_months/12:.1f} years) earlier than nominal term")
    print(f"Total interest paid:  ${total_interest:,.2f}")

    if args.show_schedule:
        print("\nPeriod  Payment     Interest   Principal   Balance")
        for row in schedule:
            print(f"{row['period']:6d}  {row['payment']:9,.2f}  {row['interest']:8,.2f}  {row['principal']:9,.2f}  {row['balance']:10,.2f}")


if __name__ == "__main__":
    main()
