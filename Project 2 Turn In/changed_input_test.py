"""Run the locked changed-input test: objective 6.50% to 7.50%."""

from app_logic import PRICES, RESERVE_ELIGIBLE, RESERVE_MINIMUM
from portfolio import estimate_from_csv, search_lowest_risk_mix


def describe(label, sleeves, correlations, objective):
    """Print a concise reproducible comparison for one estimation window."""
    result = search_lowest_risk_mix(sleeves, correlations, objective, RESERVE_ELIGIBLE, RESERVE_MINIMUM)
    print(label)
    if result is None:
        print("No feasible allocation")
        return
    print("Weights: " + " / ".join(f"{name} {weight * 100:.1f}%" for name, weight in result["weights"].items()))
    print(f"Expected return: {result['expected_return'] * 100:.2f}%")
    print(f"Volatility: {result['volatility'] * 100:.2f}%")


def main():
    """Compare the original objective with the locked changed input."""
    all_sleeves, all_correlations = estimate_from_csv(str(PRICES), False)
    stress_sleeves, stress_correlations = estimate_from_csv(str(PRICES), True)
    print("Changed input: objective return from 6.50% to 7.50%")
    describe("All months", all_sleeves, all_correlations, 0.075)
    describe("Last 36 monthly returns", stress_sleeves, stress_correlations, 0.075)


if __name__ == "__main__":
    main()
