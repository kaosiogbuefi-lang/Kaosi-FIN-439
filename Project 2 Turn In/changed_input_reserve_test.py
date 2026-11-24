"""Locked changed-input scenario: increase the reserve minimum from 3% to 90%.

This file was added with the pre-execution prediction.  It calls the current
application engine without changing the investment methodology.
"""

from app_logic import build_project2_results


def describe_window(label, result):
    """Print the feasibility and allocation result for one estimation window."""
    if result is None:
        print(f"{label}: no feasible mix meets the 6.50% net-return objective and 90.0% reserve minimum.")
        return
    weights = " / ".join(f"{name} {weight * 100:.1f}%" for name, weight in result["weights"].items())
    print(f"{label}: {weights}")
    print(f"  Expected return: {result['expected_return'] * 100:.2f}%")
    print(f"  Volatility: {result['volatility'] * 100:.2f}%")
    print(f"  Reserve-eligible weight: {result['reserve_eligible_weight'] * 100:.1f}%")


def main():
    """Run the frozen reserve-minimum scenario through the current app logic."""
    results = build_project2_results(reserve_minimum=0.90)
    print("Changed input: reserve minimum from 3.0% to 90.0%")
    describe_window("All-months base window", results["base"])
    describe_window("Last-36-returns stress window", results["stress"])
    recommendation = results["recommendation"]
    print(f"Recommendation: {recommendation['action']}")
    print(f"Reason: {recommendation['reason']}")


if __name__ == "__main__":
    main()
