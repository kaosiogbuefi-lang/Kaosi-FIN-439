"""Lab 14 - Meridian portfolio return and risk engine.

Run with: python portfolio.py
All returns, volatilities, and weights are stored as decimal values.
"""

from math import sqrt


# Editable inputs
SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"expected_return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00,
        "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05,
        "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10,
        "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80,
        "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05,
        "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00,
        "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00,
        "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25,
        "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def sleeve_names(sleeves):
    """Return sleeve names in their input order."""
    return list(sleeves)


def validate_correlations(names, correlations):
    """Raise ValueError unless correlations are complete, bounded, and symmetric."""
    for left in names:
        if left not in correlations:
            raise ValueError(f"Correlation table is missing row: {left}")
        for right in names:
            if right not in correlations[left]:
                raise ValueError(f"Correlation table is missing {left} / {right}")
            value = correlations[left][right]
            if not -1 <= value <= 1:
                raise ValueError(
                    f"Correlation for {left} / {right} must be between -1 and 1; got {value}."
                )
            if abs(value - correlations.get(right, {}).get(left, float("inf"))) > 1e-12:
                raise ValueError(f"Correlation table is not symmetric at {left} / {right}.")


def covariance_matrix(names, sleeves, correlations):
    """Build covariance = correlation * left volatility * right volatility."""
    return [
        [
            correlations[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in names
        ]
        for left in names
    ]


def equal_weight_portfolio(names):
    """Give every sleeve the same weight."""
    return {name: 1 / len(names) for name in names}


def inverse_volatility_portfolio(names, sleeves):
    """Weight sleeves proportional to inverse volatility."""
    inverse_volatilities = {name: 1 / sleeves[name]["volatility"] for name in names}
    total = sum(inverse_volatilities.values())
    return {name: inverse_volatilities[name] / total for name in names}


def portfolio_return(weights, sleeves):
    """Calculate a weighted expected return."""
    return sum(weights[name] * sleeves[name]["expected_return"] for name in weights)


def portfolio_variance(weights, names, covariance):
    """Calculate w' C w, including every cross-asset covariance term."""
    return sum(
        weights[left] * weights[right] * covariance[i][j]
        for i, left in enumerate(names)
        for j, right in enumerate(names)
    )


def portfolio_volatility(weights, names, covariance):
    """Return the square root of portfolio variance."""
    return sqrt(portfolio_variance(weights, names, covariance))


def reserve_eligible_weight(weights, reserve_eligible):
    """Sum weights in reserve-eligible sleeves."""
    return sum(weights.get(name, 0) for name in reserve_eligible)


def print_portfolio(name, weights, names, sleeves, covariance, objective_return):
    """Print one complete portfolio result."""
    weight_text = " / ".join(f"{weights[asset] * 100:.1f}" for asset in names)
    expected_return = portfolio_return(weights, sleeves)
    volatility = portfolio_volatility(weights, names, covariance)
    reserve_weight = reserve_eligible_weight(weights, RESERVE_ELIGIBLE)
    meets_objective = expected_return >= objective_return

    print(f"\n{name}")
    print(f"Weights (bills / 10-year / IG / equity): {weight_text}")
    print(f"Expected return: {expected_return * 100:.2f}%")
    print(f"Volatility: {volatility * 100:.2f}%")
    print(f"Reserve-eligible weight: {reserve_weight * 100:.1f}%")
    print(f"Meets {objective_return * 100:.1f}% objective: {'yes' if meets_objective else 'no'}")


def main():
    names = sleeve_names(SLEEVES)
    validate_correlations(names, CORRELATIONS)
    covariance = covariance_matrix(names, SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": {
            "Treasury bills": 0.0,
            "Treasury 10-year note": 0.0,
            "Investment-grade bond fund": 0.40,
            "Global equity index fund": 0.60,
        },
        "Equal weight": equal_weight_portfolio(names),
        "Inverse volatility": inverse_volatility_portfolio(names, SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, names, SLEEVES, covariance, OBJECTIVE_RETURN)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Input error: {error}")
