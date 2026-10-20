"""Project 1 MCD FCFF DCF (USD millions except per-share data)."""

from statistics import median

# ---- Evidence-based base year and editable assumptions ----
opening = {
    "revenue": 26885.0, "inventory": 61.0, "ppe": 28241.0,
    "other_assets": 30439.0, "cash": 774.0, "debt": 39973.0,
    "other_liabilities": 21333.0, "equity": -1791.0,
}
years = [2026, 2027, 2028, 2029, 2030]
growth_rates = [0.040, 0.040, 0.035, 0.030, 0.025]
gross_margin = 0.5951
sga_as_pct_gross_profit = 0.190
depreciation_rate = 2199.0 / 28241.0
capex = [3800.0, 4200.0, 4000.0, 3900.0, 3900.0]
tax_rate = 0.22
inventory_as_pct_revenue = 61.0 / 26885.0
other_working_capital_as_pct_revenue_change = 0.008
annual_debt_repayment = 250.0
annual_share_buyback = 1500.0
minimum_operating_cash = 500.0
shares_diluted = 712.3
market_price = 238.32

# WACC inputs: use values consistently with the FCFF/enterprise-value framework.
cost_of_equity = 0.080
pre_tax_cost_of_debt = 1548.0 / 39973.0
terminal_growth = 0.025


def balance_gap(row):
    assets = row["inventory"] + row["ppe"] + row["other_assets"] + row["cash"]
    liabilities_equity = row["debt"] + row["other_liabilities"] + row["equity"]
    return assets - liabilities_equity


def weighted_average_cost_of_capital(discount_equity_price=market_price):
    equity_market_value = discount_equity_price * shares_diluted
    total_capital = equity_market_value + opening["debt"]
    equity_weight = equity_market_value / total_capital
    debt_weight = opening["debt"] / total_capital
    return equity_weight * cost_of_equity + debt_weight * pre_tax_cost_of_debt * (1.0 - tax_rate)


def project(growth_path, gross_margin_input=None):
    """Produce linked income statement, balance sheet, cash flow, and FCFF rows."""
    if len(growth_path) != len(years):
        raise ValueError("The growth path must have exactly five annual rates.")
    margin = gross_margin if gross_margin_input is None else gross_margin_input
    rows, prior = [], opening.copy()
    for index, year in enumerate(years):
        revenue = prior["revenue"] * (1.0 + growth_path[index])
        gross_profit = revenue * margin
        sga = gross_profit * sga_as_pct_gross_profit
        depreciation = prior["ppe"] * depreciation_rate
        ebit = gross_profit - sga - depreciation
        interest = prior["debt"] * pre_tax_cost_of_debt
        pretax_income = ebit - interest
        tax = max(pretax_income, 0.0) * tax_rate
        net_income = pretax_income - tax

        inventory = revenue * inventory_as_pct_revenue
        inventory_change = inventory - prior["inventory"]
        revenue_change = revenue - prior["revenue"]
        other_nwc_change = other_working_capital_as_pct_revenue_change * revenue_change
        other_assets = prior["other_assets"] + other_nwc_change
        ppe = prior["ppe"] + capex[index] - depreciation
        debt = prior["debt"] - annual_debt_repayment
        equity = prior["equity"] + net_income - annual_share_buyback

        cash_from_operations = net_income + depreciation - inventory_change - other_nwc_change
        cash_from_investing = -capex[index]
        cash_from_financing = -annual_debt_repayment - annual_share_buyback
        cash = prior["cash"] + cash_from_operations + cash_from_investing + cash_from_financing
        # This simplified model permits cash below the operating minimum but flags it loudly.
        fcff = ebit * (1.0 - tax_rate) + depreciation - capex[index] - inventory_change - other_nwc_change
        row = {
            "year": year, "revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "ebit": ebit, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets, "cash": cash,
            "debt": debt, "other_liabilities": prior["other_liabilities"], "equity": equity,
            "inventory_change": inventory_change, "other_nwc_change": other_nwc_change,
            "cfo": cash_from_operations, "cfi": cash_from_investing, "cff": cash_from_financing,
            "fcff": fcff,
        }
        row["balance_gap"] = balance_gap(row)
        row["cash_tie_gap"] = cash - (prior["cash"] + cash_from_operations + cash_from_investing + cash_from_financing)
        if abs(row["balance_gap"]) > 0.05:
            raise ValueError(f"FY{year} balance-sheet check failed: {row['balance_gap']:.2f}")
        if abs(row["cash_tie_gap"]) > 0.05:
            raise ValueError(f"FY{year} cash-flow tie check failed: {row['cash_tie_gap']:.2f}")
        rows.append(row)
        prior = row
    return rows


def dcf_value(growth_path, discount_rate=None, perpetuity_growth=None, gross_margin_input=None):
    rate = weighted_average_cost_of_capital() if discount_rate is None else discount_rate
    growth = terminal_growth if perpetuity_growth is None else perpetuity_growth
    if growth >= rate:
        raise ValueError("Terminal growth must be less than WACC.")
    rows = project(growth_path, gross_margin_input)
    pv_explicit = sum(row["fcff"] / (1.0 + rate) ** (index + 1) for index, row in enumerate(rows))
    terminal_value = rows[-1]["fcff"] * (1.0 + growth) / (rate - growth)
    pv_terminal = terminal_value / (1.0 + rate) ** 5
    enterprise_value = pv_explicit + pv_terminal
    excess_cash = max(0.0, opening["cash"] - minimum_operating_cash)
    equity_value = enterprise_value + excess_cash - opening["debt"]
    per_share = equity_value / shares_diluted
    return {
        "rows": rows, "wacc": rate, "pv_explicit": pv_explicit,
        "terminal_value": terminal_value, "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value, "excess_cash": excess_cash,
        "equity_value": equity_value, "per_share": per_share,
        "terminal_share": pv_terminal / enterprise_value,
    }


def synthetic_known_answer_check():
    """Independent reconciliation to the Week 3 published training DCF case."""
    fcff, rates, rate, growth = 100.0, [0.08, 0.06, 0.05, 0.04, 0.03], 0.10, 0.03
    explicit = 0.0
    for index, annual_growth in enumerate(rates, start=1):
        fcff *= 1.0 + annual_growth
        explicit += fcff / (1.0 + rate) ** index
    terminal = fcff * (1.0 + growth) / (rate - growth)
    enterprise = explicit + terminal / (1.0 + rate) ** 5
    value_per_share = (enterprise + 50.0 - 300.0) / 50.0
    expected = 27.4974
    if abs(value_per_share - expected) > 0.0001:
        raise ValueError("Synthetic DCF reconciliation failed.")
    return value_per_share


def reverse_dcf(target_price, lower_shift=-0.05, upper_shift=0.10):
    """Find a uniform explicit-growth shift that makes DCF value equal market price."""
    def gap(shift):
        path = [rate + shift for rate in growth_rates]
        if min(path) <= -1.0:
            raise ValueError("Reverse-DCF bracket creates an annual growth rate at or below -100%.")
        return dcf_value(path)["per_share"] - target_price

    low_gap, high_gap = gap(lower_shift), gap(upper_shift)
    if low_gap * high_gap > 0:
        return None
    lower, upper = lower_shift, upper_shift
    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_gap = gap(midpoint)
        if abs(midpoint_gap) < 0.000001:
            return midpoint
        if low_gap * midpoint_gap <= 0:
            upper = midpoint
        else:
            lower, low_gap = midpoint, midpoint_gap
    return midpoint


def print_table(title, lines, rows):
    print(f"\n{title}")
    print(f"{'Line item':<32}" + "".join(f"FY{year}E".rjust(12) for year in years))
    for label, key in lines:
        print(f"{label:<32}" + "".join(f"{row[key]:>12.1f}" for row in rows))


def main():
    synthetic = synthetic_known_answer_check()
    base = dcf_value(growth_rates)
    rows = base["rows"]
    print(f"Synthetic known-answer check: ${synthetic:.4f} per share (pass)")
    print(f"Base-year balance reconciliation: {balance_gap(opening):.1f} (pass)")
    print(f"WACC: {base['wacc']:.2%}")
    print_table("Income Statement", [("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"), ("Depreciation", "depreciation"), ("EBIT", "ebit"), ("Interest", "interest"), ("Net income", "net_income")], rows)
    print_table("Balance Sheet", [("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"), ("Cash", "cash"), ("Debt", "debt"), ("Other liabilities", "other_liabilities"), ("Equity", "equity")], rows)
    print_table("Cash Flow and FCFF", [("Cash from operations", "cfo"), ("Cash from investing", "cfi"), ("Cash from financing", "cff"), ("Free cash flow to firm", "fcff")], rows)
    print("\nArticulation checks")
    for row in rows:
        print(f"FY{row['year']}E: balance gap {row['balance_gap']:.1f}; cash-flow tie gap {row['cash_tie_gap']:.1f}")
    print("\nEnterprise-value FCFF DCF")
    print(f"PV explicit FCFF: {base['pv_explicit']:.1f}")
    print(f"Terminal value at FY2030: {base['terminal_value']:.1f}")
    print(f"PV terminal value: {base['pv_terminal']:.1f}")
    print(f"Enterprise value: {base['enterprise_value']:.1f}")
    print(f"Less debt: {opening['debt']:.1f}; add excess cash: {base['excess_cash']:.1f}")
    print(f"Equity value: {base['equity_value']:.1f}; value per diluted share: ${base['per_share']:.2f}")
    print(f"Terminal value share of enterprise value: {base['terminal_share']:.1%}")

    print("\nCausal cases (uniform annual growth-rate shifts)")
    for label, shift in [("Low", -0.01), ("Base", 0.0), ("High", 0.01)]:
        result = dcf_value([rate + shift for rate in growth_rates])
        print(f"{label}: ${result['per_share']:.2f} per share")

    print("\nWACC / terminal-growth sensitivity ($ per share)")
    terminal_rates = [0.020, 0.025, 0.030]
    wacc_rates = [base["wacc"] - 0.005, base["wacc"], base["wacc"] + 0.005]
    print("WACC \\ g".ljust(12) + "".join(f"{rate:>12.1%}" for rate in terminal_rates))
    for rate in wacc_rates:
        cells = []
        for growth in terminal_rates:
            cells.append("invalid" if growth >= rate else f"${dcf_value(growth_rates, rate, growth)['per_share']:.2f}")
        print(f"{rate:.2%}".ljust(12) + "".join(f"{cell:>12}" for cell in cells))

    higher_wacc = dcf_value(growth_rates, base["wacc"] + 0.005)["per_share"]
    higher_growth = dcf_value(growth_rates, base["wacc"], terminal_growth + 0.005)["per_share"]
    if higher_wacc >= base["per_share"] or higher_growth <= base["per_share"]:
        raise ValueError("DCF monotonicity check failed.")
    print("DCF monotonicity checks: higher WACC lowers value; higher terminal growth raises value (pass)")

    implied_shift = reverse_dcf(market_price)
    print("\nReverse DCF")
    print("No solution in bracket" if implied_shift is None else f"Market price ${market_price:.2f} implies a {implied_shift:+.2%} uniform shift to Years 1–5 growth.")


if __name__ == "__main__":
    main()
