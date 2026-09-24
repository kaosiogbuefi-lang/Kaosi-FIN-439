"""Lab 10 MCD five-year pro-forma, USD millions except per-share data."""

# FY2025 opening balance sheet, simplified but reconciled to the 2025 Form 10-K.
opening = {
    "revenue": 26885.0, "inventory": 61.0, "ppe": 28241.0,
    "other_assets": 30439.0, "cash": 774.0, "debt": 39973.0,
    "revolver": 0.0, "other_liabilities": 21333.0, "equity": -1791.0,
}

# Every assumption is labelled and explained in lab-10-mcd-assumptions.md.
growth_rates = [0.04, 0.04, 0.035, 0.03, 0.025]
gross_margin = 0.5951
sga_as_pct_gross_profit = [0.190, 0.190, 0.190, 0.190, 0.190]
depreciation_as_pct_opening_ppe = 2199.0 / 28241.0
impairment = 0.0
capex = [3800.0, 4200.0, 4000.0, 3900.0, 3900.0]
tax_rate = 0.22
inventory_as_pct_revenue = 61.0 / 26885.0
other_working_capital_as_pct_revenue_change = 0.008
minimum_cash = 500.0
revolver_limit = 5000.0
revolver_rate = 0.045
annual_debt_repayment = 250.0
annual_share_buyback = 1500.0
term_debt_rate = 1548.0 / 39973.0
cost_of_equity = 0.08
terminal_growth = 0.025
shares_outstanding = 712.3
years = [2026, 2027, 2028, 2029, 2030]


def assert_balanced(year, row):
    assets = row["inventory"] + row["ppe"] + row["other_assets"] + row["cash"]
    liabilities_and_equity = row["debt"] + row["revolver"] + row["other_liabilities"] + row["equity"]
    gap = assets - liabilities_and_equity
    if abs(gap) > 0.05:
        raise ValueError(f"FY{year}E is not balanced: assets minus liabilities minus equity = {gap:.1f}")
    if row["cash"] < minimum_cash - 0.05:
        raise ValueError(f"FY{year}E cash is below the minimum: {row['cash']:.1f} < {minimum_cash:.1f}")
    return gap


def project_year(prior, year_index):
    revenue = prior["revenue"] * (1.0 + growth_rates[year_index])
    gross_profit = revenue * gross_margin
    sga = gross_profit * sga_as_pct_gross_profit[year_index]
    depreciation = prior["ppe"] * depreciation_as_pct_opening_ppe
    operating_income = gross_profit - sga - depreciation - impairment
    interest = prior["debt"] * term_debt_rate + prior["revolver"] * revolver_rate
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * tax_rate
    net_income = pretax_income - tax

    inventory = revenue * inventory_as_pct_revenue
    ppe = prior["ppe"] + capex[year_index] - depreciation
    revenue_change = revenue - prior["revenue"]
    other_working_capital_change = other_working_capital_as_pct_revenue_change * revenue_change
    other_assets = prior["other_assets"] + other_working_capital_change - impairment
    debt = prior["debt"] - annual_debt_repayment
    equity = prior["equity"] + net_income - annual_share_buyback
    fcfe = (net_income + depreciation + impairment - capex[year_index]
            - (inventory - prior["inventory"]) - other_working_capital_change - annual_debt_repayment)
    cash_before_revolver = prior["cash"] + fcfe - annual_share_buyback
    revolver = prior["revolver"]
    if cash_before_revolver < minimum_cash:
        draw = minimum_cash - cash_before_revolver
        if revolver + draw > revolver_limit:
            raise ValueError("revolver limit exceeded while maintaining minimum cash")
        revolver += draw
        cash = minimum_cash
    else:
        repayment = min(revolver, cash_before_revolver - minimum_cash)
        revolver -= repayment
        cash = cash_before_revolver - repayment
    return {"revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "impairment": impairment,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
            "cash": cash, "debt": debt, "revolver": revolver,
            "other_liabilities": prior["other_liabilities"], "equity": equity,
            "other_working_capital_change": other_working_capital_change, "fcfe": fcfe}


def print_table(title, lines, rows):
    print(f"\n{title}")
    print(f"{'Line item':<34}" + "".join(f"FY{year}E".rjust(12) for year in years))
    for label, key in lines:
        print(f"{label:<34}" + "".join(f"{row[key]:>12.1f}" for row in rows))


def main():
    if terminal_growth >= cost_of_equity:
        raise SystemExit("Terminal growth must be less than cost of equity.")
    rows, prior = [], opening.copy()
    for index, year in enumerate(years):
        row = project_year(prior, index)
        row["year"] = year
        row["gap"] = assert_balanced(year, row)
        rows.append(row)
        prior = row

    print_table("Income Statement", [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("SG&A", "sga"), ("Depreciation", "depreciation"), ("Operating income", "operating_income"),
        ("Interest expense", "interest"), ("Pretax income", "pretax_income"), ("Tax", "tax"),
        ("Net income", "net_income")], rows)
    print_table("Balance Sheet", [("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
        ("Cash", "cash"), ("Debt", "debt"), ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"), ("Equity", "equity")], rows)
    print_table("Cash Flow / FCFE", [("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Capital spending", "capex"), ("Change in inventory", "inventory_change"),
        ("Change in other working capital", "other_working_capital_change"),
        ("Debt repayment", "debt_repayment"), ("Free cash flow to equity", "fcfe")], [
            {**row, "capex": capex[i], "inventory_change": row["inventory"] - (opening if i == 0 else rows[i - 1])["inventory"],
             "debt_repayment": annual_debt_repayment} for i, row in enumerate(rows)])
    print("\nChecks")
    for row in rows:
        print(f"FY{row['year']}E: assets − liabilities − equity = {row['gap']:.1f}; cash >= minimum = {row['cash'] >= minimum_cash}")
    pv_fcfe = sum(row["fcfe"] / (1 + cost_of_equity) ** (i + 1) for i, row in enumerate(rows))
    terminal_value = (rows[-1]["fcfe"] + annual_debt_repayment) * (1 + terminal_growth) / (cost_of_equity - terminal_growth)
    pv_terminal = terminal_value / (1 + cost_of_equity) ** 5
    equity_value = pv_fcfe + pv_terminal
    print("\nEquity Valuation")
    print(f"Equity value: {equity_value:.2f}")
    print(f"Share of value after 2030: {pv_terminal / equity_value:.2%}")
    print(f"Value per share: ${equity_value / shares_outstanding:.2f}")


if __name__ == "__main__":
    main()
