"""Lab 11 one-at-a-time sensitivity analysis for the MCD pro-forma."""

import importlib.util
from pathlib import Path


SOURCE_MODEL = Path(__file__).with_name("lab 10mcd_proforma.py")
SPEC = importlib.util.spec_from_file_location("mcd_proforma", SOURCE_MODEL)
model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(model)

BASE_GROWTH = [0.04, 0.04, 0.035, 0.03, 0.025]
LOW_GROWTH = [value - 0.01 for value in BASE_GROWTH]
HIGH_GROWTH = [value + 0.01 for value in BASE_GROWTH]
BASE_MARGIN, LOW_MARGIN, HIGH_MARGIN = 0.5951, 0.5850, 0.6050


def run_model(growths, margin):
    """Fresh independent model run; no input changes persist between cases."""
    saved_growths, saved_margin = model.growth_rates, model.gross_margin
    model.growth_rates, model.gross_margin = list(growths), margin
    try:
        rows, prior = [], model.opening.copy()
        for index, year in enumerate(model.years):
            row = model.project_year(prior, index)
            row["year"] = year
            row["gap"] = model.assert_balanced(year, row)
            rows.append(row)
            prior = row
        pv_fcfe = sum(row["fcfe"] / (1 + model.cost_of_equity) ** (i + 1) for i, row in enumerate(rows))
        terminal = (rows[-1]["fcfe"] + model.annual_debt_repayment) * (1 + model.terminal_growth) / (model.cost_of_equity - model.terminal_growth)
        equity_value = pv_fcfe + terminal / (1 + model.cost_of_equity) ** 5
        return rows, equity_value / model.shares_outstanding
    finally:
        model.growth_rates, model.gross_margin = saved_growths, saved_margin


def make_row(label, actual_input, result, base):
    rows, value = result
    base_rows, base_value = base
    final, base_final = rows[-1], base_rows[-1]
    return (label, actual_input, final["operating_income"], final["fcfe"], value,
            final["operating_income"] - base_final["operating_income"],
            final["fcfe"] - base_final["fcfe"], value - base_value,
            all(abs(row["gap"]) <= 0.05 and row["cash"] >= model.minimum_cash - 0.05 for row in rows))


def print_driver(title, rows):
    print(f"\n{title}")
    print(f"{'Run':<8}{'Actual input':<42}{'2030 operating income':>24}{'2030 FCFE':>16}{'Value/share':>16}")
    for label, actual, oi, fcfe, value, oi_delta, fcfe_delta, value_delta, checks_pass in rows:
        print(f"{label:<8}{actual:<42}{oi:>24.1f}{fcfe:>16.1f}{value:>16.2f}  {'pass' if checks_pass else 'INVALID'}")
        print(f"{'change from base':<50}{oi_delta:>24.1f}{fcfe_delta:>16.1f}{value_delta:>16.2f}")
    print("Span (maximum - minimum): "
          f"operating income {max(row[2] for row in rows) - min(row[2] for row in rows):.1f}; "
          f"FCFE {max(row[3] for row in rows) - min(row[3] for row in rows):.1f}; "
          f"value/share ${max(row[4] for row in rows) - min(row[4] for row in rows):.2f}")


def main():
    base = run_model(BASE_GROWTH, BASE_MARGIN)
    growth_rows = [
        make_row("lower", "3.0%, 3.0%, 2.5%, 2.0%, 1.5%", run_model(LOW_GROWTH, BASE_MARGIN), base),
        make_row("base", "4.0%, 4.0%, 3.5%, 3.0%, 2.5%", base, base),
        make_row("higher", "5.0%, 5.0%, 4.5%, 4.0%, 3.5%", run_model(HIGH_GROWTH, BASE_MARGIN), base),
    ]
    margin_rows = [
        make_row("lower", "58.50% every forecast year", run_model(BASE_GROWTH, LOW_MARGIN), base),
        make_row("base", "59.51% every forecast year", base, base),
        make_row("higher", "60.50% every forecast year", run_model(BASE_GROWTH, HIGH_MARGIN), base),
    ]
    print_driver("Revenue-growth sensitivity", growth_rows)
    print_driver("Gross-margin sensitivity", margin_rows)
    restored = run_model(BASE_GROWTH, BASE_MARGIN)[1]
    print(f"\nRestored-base check: ${restored:.2f} per share; matches original base = {abs(restored - base[1]) < 0.005}")


if __name__ == "__main__":
    main()
