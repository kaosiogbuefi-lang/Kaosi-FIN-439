"""Lab 14 - Meridian portfolio return and risk engine.

Run with: python portfolio.py
All returns, volatilities, and weights are stored as decimal values.
"""

import csv
from math import sqrt
from statistics import mean, stdev


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
            # Permit only machine-rounding noise around the mathematical bounds.
            # A meaningful invalid input (for example 1.3) remains an error.
            if value < -1 - 1e-12 or value > 1 + 1e-12:
                raise ValueError(
                    f"Correlation for {left} / {right} must be between -1 and 1; got {value}."
                )
            if value > 1:
                correlations[left][right] = 1.0
                value = 1.0
            elif value < -1:
                correlations[left][right] = -1.0
                value = -1.0
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


def search_lowest_risk_mix(
    sleeves, correlations, objective_return, reserve_eligible, reserve_minimum, step=0.05
):
    """Return the lowest-volatility long-only step-size mix that meets both rules.

    All inputs and returned weights are decimals: 0.05 represents five percentage points.
    Return None when no candidate can meet the objective and reserve minimum.
    """
    names = sleeve_names(sleeves)
    validate_correlations(names, correlations)
    if step <= 0 or abs(round(1 / step) * step - 1) > 1e-12:
        raise ValueError("Step must divide 100% exactly, such as 0.05.")
    if not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0% and 100%.")

    covariance = covariance_matrix(names, sleeves, correlations)
    units = round(1 / step)
    best = None

    def try_weights(index, units_left, chosen_units):
        nonlocal best
        if index == len(names) - 1:
            weight_units = chosen_units + [units_left]
            weights = {name: unit * step for name, unit in zip(names, weight_units)}
            expected_return = portfolio_return(weights, sleeves)
            reserve_weight = reserve_eligible_weight(weights, reserve_eligible)
            if expected_return < objective_return or reserve_weight < reserve_minimum:
                return
            volatility = portfolio_volatility(weights, names, covariance)
            result = {
                "weights": weights,
                "expected_return": expected_return,
                "volatility": volatility,
                "reserve_eligible_weight": reserve_weight,
            }
            if best is None or result["volatility"] < best["volatility"]:
                best = result
            return

        for unit in range(units_left + 1):
            try_weights(index + 1, units_left - unit, chosen_units + [unit])

    try_weights(0, units, [])
    return best


def estimate_from_csv(csv_source, last_36_months=False):
    """Estimate annualized return, volatility, and correlation from monthly prices.

    csv_source can be a path or an uploaded text/binary file. Its first column is a date,
    prices are oldest first, and every later column is an asset name.
    """
    close_after_read = False
    if isinstance(csv_source, (str, bytes)):
        csv_source = open(csv_source, newline="", encoding="utf-8-sig")
        close_after_read = True
    try:
        if hasattr(csv_source, "seek"):
            csv_source.seek(0)
        rows = list(csv.reader(_text_lines(csv_source)))
    finally:
        if close_after_read:
            csv_source.close()

    if len(rows) < 3 or len(rows[0]) < 2:
        raise ValueError("CSV needs a date column, at least one asset column, and three price rows.")
    names = rows[0][1:]
    if not all(names) or len(set(names)) != len(names):
        raise ValueError("Each asset column needs a unique header.")
    prices = {name: [] for name in names}
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(names) + 1:
            raise ValueError(f"CSV row {row_number} has the wrong number of columns.")
        for name, value in zip(names, row[1:]):
            price = float(value)
            if price <= 0:
                raise ValueError(f"CSV row {row_number}, {name} must be positive.")
            prices[name].append(price)
    monthly_returns = {
        name: [later / earlier - 1 for earlier, later in zip(values, values[1:])]
        for name, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {name: values[-36:] for name, values in monthly_returns.items()}
    if len(next(iter(monthly_returns.values()))) < 2:
        raise ValueError("CSV needs at least three monthly returns for an estimate.")

    sleeves = {
        name: {"expected_return": mean(values) * 12, "volatility": stdev(values) * sqrt(12)}
        for name, values in monthly_returns.items()
    }
    correlations = {
        left: {
            right: _correlation(monthly_returns[left], monthly_returns[right])
            for right in names
        }
        for left in names
    }
    return sleeves, correlations


def _text_lines(file_object):
    """Yield decoded text lines from a normal file or Streamlit upload."""
    for line in file_object:
        yield line.decode("utf-8-sig") if isinstance(line, bytes) else line


def _correlation(left_values, right_values):
    """Return the sample correlation of two equal-length data series."""
    left_std = stdev(left_values)
    right_std = stdev(right_values)
    if left_std == 0 or right_std == 0:
        raise ValueError("Cannot calculate correlation when an asset has zero volatility.")
    left_mean = mean(left_values)
    right_mean = mean(right_values)
    covariance = sum(
        (left - left_mean) * (right - right_mean)
        for left, right in zip(left_values, right_values)
    ) / (len(left_values) - 1)
    # A series correlated with itself can calculate as 1.0000000000000002
    # because of binary floating-point rounding. Clamp only this derived value;
    # validate_correlations still rejects invalid user-entered table values.
    return max(-1.0, min(1.0, covariance / (left_std * right_std)))


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
