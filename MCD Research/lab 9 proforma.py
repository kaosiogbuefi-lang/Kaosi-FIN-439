"""Lab 09 ABG three-statement engine (USD millions, except per-share data)."""

# Opening balance sheet: FY2025 actual.
opening = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}

# Assumptions from Lab 09 Part 1.
revenue_growth = 0.018
gross_margin = 0.1705
sga_as_pct_gross_profit = [0.665, 0.655, 0.645, 0.645, 0.645]
depreciation_as_pct_opening_ppe = 82.4 / 3070.4
impairment = 120.0
capex = 250.0
tax_rate = 0.255
inventory_days = 2135.8 / (17999.0 - 3071.7) * 365
floor_plan_as_pct_inventory = 2027.0 / 2135.8
other_working_capital_as_pct_revenue_change = 0.008
minimum_cash = 25.0
revolver_limit = 850.0
revolver_rate = 0.06
annual_debt_repayment = 150.0
annual_share_buyback = 150.0
floor_plan_rate = 0.0467
term_debt_rate = 0.0544
cost_of_equity = 0.10
terminal_growth = 0.025
shares_outstanding = 17.951349
years = [2026, 2027, 2028, 2029, 2030]


def assert_balanced(year, statement):
    """Refuse a model year with a balance-sheet gap or sub-minimum cash."""
    assets = statement["inventory"] + statement["ppe"] + statement["other_assets"] + statement["cash"]
    liabilities_and_equity = (
        statement["floor_plan"]
        + statement["term_debt"]
        + statement["revolver"]
        + statement["other_liabilities"]
        + statement["equity"]
    )
    gap = assets - liabilities_and_equity
    if abs(gap) > 0.05:
        raise ValueError(f"FY{year}E is not balanced: assets minus liabilities minus equity = {gap:.1f}")
    if statement["cash"] < minimum_cash - 0.05:
        raise ValueError(f"FY{year}E cash is below the minimum: {statement['cash']:.1f} < {minimum_cash:.1f}")
    return gap


def project_year(prior, sga_ratio):
    """Project one year in the instruction's required income/BS/FCFE/cash order."""
    revenue = prior["revenue"] * (1.0 + revenue_growth)
    gross_profit = revenue * gross_margin
    sga = gross_profit * sga_ratio
    depreciation = prior["ppe"] * depreciation_as_pct_opening_ppe
    operating_income = gross_profit - sga - depreciation - impairment
    interest = (
        prior["floor_plan"] * floor_plan_rate
        + prior["term_debt"] * term_debt_rate
        + prior["revolver"] * revolver_rate
    )
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * tax_rate
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * inventory_days / 365.0
    floor_plan = inventory * floor_plan_as_pct_inventory
    ppe = prior["ppe"] + capex - depreciation
    revenue_change = revenue - prior["revenue"]
    other_working_capital_change = other_working_capital_as_pct_revenue_change * revenue_change
    other_assets = prior["other_assets"] + other_working_capital_change - impairment
    term_debt = prior["term_debt"] - annual_debt_repayment
    other_liabilities = prior["other_liabilities"]
    equity = prior["equity"] + net_income - annual_share_buyback

    fcfe = (
        net_income
        + depreciation
        + impairment
        - capex
        - (inventory - prior["inventory"])
        - other_working_capital_change
        + (floor_plan - prior["floor_plan"])
        - annual_debt_repayment
    )
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

    return {
        "revenue": revenue,
        "gross_profit": gross_profit,
        "sga": sga,
        "depreciation": depreciation,
        "impairment": impairment,
        "operating_income": operating_income,
        "interest": interest,
        "pretax_income": pretax_income,
        "tax": tax,
        "net_income": net_income,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "cash": cash,
        "floor_plan": floor_plan,
        "term_debt": term_debt,
        "revolver": revolver,
        "other_liabilities": other_liabilities,
        "equity": equity,
        "other_working_capital_change": other_working_capital_change,
        "fcfe": fcfe,
    }


def print_statement(title, lines, projections):
    print(f"\n{title}")
    print(f"{'Line item':<34}" + "".join(f"FY{year}E".rjust(12) for year in years))
    for label, key in lines:
        print(f"{label:<34}" + "".join(f"{row[key]:>12.1f}" for row in projections))


def main():
    if terminal_growth >= cost_of_equity:
        raise SystemExit("Terminal growth must be less than the cost of equity.")

    projections = []
    prior = opening.copy()
    for year, sga_ratio in zip(years, sga_as_pct_gross_profit):
        statement = project_year(prior, sga_ratio)
        statement["year"] = year
        statement["balance_gap"] = assert_balanced(year, statement)
        projections.append(statement)
        prior = statement

    print_statement(
        "Income Statement",
        [("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
         ("Depreciation", "depreciation"), ("Impairment", "impairment"),
         ("Operating income", "operating_income"), ("Interest expense", "interest"),
         ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income")],
        projections,
    )
    print_statement(
        "Balance Sheet",
        [("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
         ("Cash", "cash"), ("Floor plan", "floor_plan"), ("Term debt", "term_debt"),
         ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity")],
        projections,
    )
    print_statement(
        "Cash Flow / FCFE",
        [("Net income", "net_income"), ("Depreciation", "depreciation"), ("Impairment", "impairment"),
         ("Capital spending", "capex"), ("Change in inventory", "inventory_change"),
         ("Change in other working capital", "other_working_capital_change"),
         ("Change in floor plan", "floor_plan_change"), ("Debt repayment", "debt_repayment"),
         ("Free cash flow to equity", "fcfe")],
        [
            {
                **row,
                "capex": capex,
                "inventory_change": row["inventory"] - (opening if index == 0 else projections[index - 1])["inventory"],
                "floor_plan_change": row["floor_plan"] - (opening if index == 0 else projections[index - 1])["floor_plan"],
                "debt_repayment": annual_debt_repayment,
            }
            for index, row in enumerate(projections)
        ],
    )

    print("\nChecks")
    for row in projections:
        print(f"FY{row['year']}E: assets − liabilities − equity = {row['balance_gap']:.1f}; cash >= minimum = {row['cash'] >= minimum_cash}")

    present_value_fcfe = sum(row["fcfe"] / (1.0 + cost_of_equity) ** (index + 1) for index, row in enumerate(projections))
    terminal_value = (projections[-1]["fcfe"] + annual_debt_repayment) * (1.0 + terminal_growth) / (cost_of_equity - terminal_growth)
    present_value_terminal = terminal_value / (1.0 + cost_of_equity) ** 5
    equity_value = present_value_fcfe + present_value_terminal
    print("\nEquity Valuation")
    print(f"Equity value: {equity_value:.2f}")
    print(f"Share of value after 2030: {present_value_terminal / equity_value:.2%}")
    print(f"Value per share: ${equity_value / shares_outstanding:.2f}")


if __name__ == "__main__":
    main()
