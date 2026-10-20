"""Lab 13 - Meridian Foundation Reserve mandate checker.

Run with: python mandate.py
All monetary inputs are USD millions; portfolio weights are percentages.
"""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "days_to_redeem": 0, "reserve_eligible": True},
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "days_to_redeem": 1,
        "reserve_eligible": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "days_to_redeem": 1,
        "reserve_eligible": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "days_to_redeem": 2,
        "reserve_eligible": False,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "days_to_redeem": 3,
        "reserve_eligible": False,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "days_to_redeem": 90,
        "reserve_eligible": False,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "days_to_redeem": 4,
        "reserve_eligible": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "days_to_redeem": 1,
        "reserve_eligible": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Deliberately conservative attack portfolio: it passes the coded rules but
    # may not be able to pursue the return objective in S2.
    "D": {
        "Cash": 90, "Treasury bills": 3, "Treasury 10-year note": 0,
        "Global equity index fund": 7, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    # Meridian's own benchmark: 40% investment-grade bonds, 60% equity.
    "E": {
        "Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 60, "Investment-grade bond fund": 40,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def total_for(candidate, predicate):
    """Return the weight of holdings whose metadata satisfies predicate."""
    return sum(weight for holding, weight in candidate.items() if predicate(HOLDINGS[holding]))


def largest_single_company(candidate):
    """Aggregate each non-exempt issuer before finding the largest exposure."""
    issuer_weights = {}
    for holding, weight in candidate.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            issuer_weights[issuer] = issuer_weights.get(issuer, 0) + weight
    return max(issuer_weights.values(), default=0)


def print_rule(label, value, passed):
    print(f"{label}: {value:.1f} {'pass' if passed else 'FAIL'}")
    return not passed


def check_candidate(name, candidate, reserve_minimum):
    print(f"\nCandidate {name}")
    failures = 0

    weight_sum = sum(candidate.values())
    failures += print_rule("Weights sum to 100", weight_sum, weight_sum == 100)

    lowest_weight = min(candidate.values())
    failures += print_rule("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0)

    reserve_weight = total_for(candidate, lambda data: data["reserve_eligible"])
    failures += print_rule(
        f"Reserve >= {reserve_minimum:.1f}%", reserve_weight, reserve_weight >= reserve_minimum
    )

    liquid_weight = total_for(
        candidate, lambda data: data["days_to_redeem"] <= LIQUIDITY_WINDOW
    )
    failures += print_rule(
        f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
        liquid_weight,
        liquid_weight >= MINIMUM_LIQUID_SHARE,
    )

    largest_company = largest_single_company(candidate)
    failures += print_rule(
        f"Largest single company <= {ISSUER_LIMIT:.1f}%",
        largest_company,
        largest_company <= ISSUER_LIMIT,
    )
    print("Calendar-year loss: requires CIO clarification")
    if failures == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failures} rule(s)")


def main():
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")
    for name, candidate in CANDIDATES.items():
        check_candidate(name, candidate, reserve_minimum)


if __name__ == "__main__":
    main()
