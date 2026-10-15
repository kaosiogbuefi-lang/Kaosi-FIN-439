"""Meridian Foundation Reserve mandate checker; standard library only."""

# Editable inputs
holdings = [
    {"holding": "Cash", "issuer": "none", "days": 0, "reserve_eligible": True},
    {"holding": "Treasury bills", "issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    {"holding": "Treasury 10-year note", "issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    {"holding": "Global equity index fund", "issuer": "diversified fund", "days": 2, "reserve_eligible": False},
    {"holding": "Investment-grade bond fund", "issuer": "diversified fund", "days": 3, "reserve_eligible": False},
    {"holding": "Private real estate fund", "issuer": "diversified fund", "days": 90, "reserve_eligible": False},
    {"holding": "Acme Corp bonds", "issuer": "Acme Corp", "days": 4, "reserve_eligible": False},
    {"holding": "Acme Corp stock", "issuer": "Acme Corp", "days": 1, "reserve_eligible": False},
]

candidates = {
    "A": {"Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
          "Global equity index fund": 60, "Investment-grade bond fund": 26,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
    "B": {"Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
          "Global equity index fund": 55, "Investment-grade bond fund": 20,
          "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4},
    "C": {"Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
          "Global equity index fund": 70, "Investment-grade bond fund": 20,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8},
    # AI attack candidate: passes the mechanical rules but may not meet S2's return objective.
    "D": {"Cash": 3, "Treasury bills": 87, "Treasury 10-year note": 0,
          "Global equity index fund": 10, "Investment-grade bond fund": 0,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
}

reserve_size = 100.0  # USD millions
quarterly_distribution = 0.75  # USD millions
quarters_to_cover = 4
liquidity_window = 5  # business days
minimum_liquid_share = 90.0  # percent
issuer_limit = 8.0  # percent
exempt_issuers = {"none", "U.S. Treasury", "diversified fund"}


def status(condition):
    return "pass" if condition else "FAIL"


def holding_lookup():
    return {item["holding"]: item for item in holdings}


def issuer_weights(weights, lookup):
    totals = {}
    for holding, weight in weights.items():
        issuer = lookup[holding]["issuer"]
        if issuer not in exempt_issuers:
            totals[issuer] = totals.get(issuer, 0.0) + weight
    return totals


def check_candidate(name, weights, reserve_minimum, lookup):
    values = list(weights.values())
    total_weight = sum(values)
    lowest_weight = min(values)
    reserve_weight = sum(
        weight for holding, weight in weights.items() if lookup[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight for holding, weight in weights.items() if lookup[holding]["days"] <= liquidity_window
    )
    company_weights = issuer_weights(weights, lookup)
    largest_company = max(company_weights.values(), default=0.0)

    checks = [
        ("Weights sum to 100", total_weight, total_weight == 100.0),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0.0),
        (f"Reserve ≥ {reserve_minimum:.1f}%", reserve_weight, reserve_weight >= reserve_minimum),
        (f"Redeemable in {liquidity_window} days ≥ {minimum_liquid_share:.1f}%", liquid_weight, liquid_weight >= minimum_liquid_share),
        (f"Largest single company ≤ {issuer_limit:.1f}%", largest_company, largest_company <= issuer_limit),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, value, passed in checks:
        print(f"{label}: {value:.1f} {status(passed)}")
        failures += not passed
    print("Calendar-year loss: requires CIO clarification")
    if failures:
        print(f"Verdict: fails {failures} rule(s)")
    else:
        print("Verdict: passes every checkable rule")


def main():
    reserve_minimum = quarters_to_cover * quarterly_distribution / reserve_size * 100.0
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    lookup = holding_lookup()
    for name, weights in candidates.items():
        check_candidate(name, weights, reserve_minimum, lookup)


if __name__ == "__main__":
    main()
