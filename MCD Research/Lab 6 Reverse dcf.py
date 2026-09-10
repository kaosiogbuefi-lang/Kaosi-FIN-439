"""Five-year FCFF DCF for McDonald's (USD millions except per-share data)."""

# Editable inputs (USD millions unless otherwise noted)
starting_fcff = 9022.0
growth_rates = [0.06, 0.055, 0.05, 0.045, 0.04]
wacc = 0.07
terminal_growth = 0.025
non_operating_cash = 822.0
debt = 38300.0
diluted_shares = 712.3  # millions

# Lab 06 sensitivity and reverse-DCF inputs
sensitivity_waccs = [0.06, 0.07, 0.08]
sensitivity_terminal_growths = [0.02, 0.025, 0.03]
target_share_price = 253.48
reverse_shift_lower_bound = -0.05
reverse_shift_upper_bound = 0.10


def value_per_share(discount_rate, perpetual_growth, growth_shift=0.0):
    if perpetual_growth >= discount_rate:
        raise ValueError("terminal growth must be less than WACC")
    fcff = starting_fcff
    pv_explicit = 0.0
    for year_number, growth_rate in enumerate(growth_rates, start=1):
        adjusted_growth = growth_rate + growth_shift
        if adjusted_growth <= -1.0:
            raise ValueError("a growth rate of -100% or below is not allowed")
        fcff *= 1.0 + adjusted_growth
        pv_explicit += fcff / (1.0 + discount_rate) ** year_number
    terminal_value = fcff * (1.0 + perpetual_growth) / (discount_rate - perpetual_growth)
    pv_terminal = terminal_value / (1.0 + discount_rate) ** 5
    enterprise_value = pv_explicit + pv_terminal
    return (enterprise_value + non_operating_cash - debt) / diluted_shares


def print_base_case():
    fcff_by_year = []
    fcff = starting_fcff
    for growth_rate in growth_rates:
        fcff *= 1.0 + growth_rate
        fcff_by_year.append(fcff)

    pv_explicit = sum(
        year_fcff / (1.0 + wacc) ** year_number
        for year_number, year_fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value = fcff_by_year[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1.0 + wacc) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + non_operating_cash - debt

    for year_number, year_fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year_number}: {year_fcff:.4f}")
    print(f"PV of Five Explicit FCFF: {pv_explicit:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value:.4f}")
    print(f"PV of Terminal Value: {pv_terminal:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {equity_value / diluted_shares:.4f}")
    print(f"PV of Terminal Value as Share of Enterprise Value: {pv_terminal / enterprise_value:.4f}")


def print_sensitivity_grid():
    print("\nSensitivity Grid: Value per Diluted Share")
    print("WACC \\ Terminal Growth | " + " | ".join(
        f"{growth:.1%}" for growth in sensitivity_terminal_growths
    ))
    for discount_rate in sensitivity_waccs:
        cells = []
        for perpetual_growth in sensitivity_terminal_growths:
            if perpetual_growth >= discount_rate:
                cells.append("invalid")
            else:
                cells.append(f"${value_per_share(discount_rate, perpetual_growth):.2f}")
        print(f"{discount_rate:.1%}".ljust(24) + " | " + " | ".join(cells))


def solve_reverse_dcf():
    lower = reverse_shift_lower_bound
    upper = reverse_shift_upper_bound
    try:
        lower_gap = value_per_share(wacc, terminal_growth, lower) - target_share_price
        upper_gap = value_per_share(wacc, terminal_growth, upper) - target_share_price
    except ValueError as error:
        print(f"\nReverse DCF: no solution — {error}.")
        return

    if lower_gap * upper_gap > 0.0:
        print("\nReverse DCF: no solution in the specified bracket.")
        print(f"Target Share Price: ${target_share_price:.2f}")
        print(f"Search Bracket: {lower:.2%} to {upper:.2%}")
        return

    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_gap = value_per_share(wacc, terminal_growth, midpoint) - target_share_price
        if abs(midpoint_gap) < 0.000001:
            break
        if lower_gap * midpoint_gap <= 0.0:
            upper = midpoint
        else:
            lower = midpoint
            lower_gap = midpoint_gap

    print("\nReverse DCF: Uniform Five-Year Growth-Rate Shift")
    print(f"Solved Shift: {midpoint:.4%}")
    print(f"Target Share Price: ${target_share_price:.2f}")
    print("Held Fixed: starting FCFF, WACC, terminal growth, non-operating cash, debt, diluted shares, and the relative five-year growth pattern.")


def main():
    if terminal_growth >= wacc:
        raise SystemExit("Error: terminal growth must be less than WACC for the Gordon-growth terminal value.")
    print_base_case()
    print_sensitivity_grid()
    solve_reverse_dcf()


if __name__ == "__main__":
    main()
