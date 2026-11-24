"""Reusable calculations and decision logic for the Project 2 portfolio app."""

import csv
from calendar import monthrange
from datetime import date
from io import StringIO
from itertools import product
from math import floor, isfinite
from pathlib import Path

from portfolio import (
    covariance_matrix,
    equal_weight_portfolio,
    estimate_from_csv,
    inverse_volatility_portfolio,
    portfolio_return,
    portfolio_volatility,
    reserve_eligible_weight,
    search_lowest_risk_mix,
    sleeve_names,
)


OBJECTIVE = 0.065
RESERVE_MINIMUM = 0.03
RESERVE_ELIGIBLE = {"BIL", "IEF"}
STABILITY_THRESHOLD_POINTS = 25.0
STABILITY_COMPARISON_TOLERANCE_POINTS = 1e-9
ORIGINAL_RESERVE_MINIMUM = 0.03
PRICES = Path(__file__).with_name("prices.csv")
EXPECTED_TICKERS = ("BIL", "IEF", "LQD", "VT")
PRICE_DOWNLOAD_DATE = date(2026, 10, 22)
EXECUTABLE_WEIGHT_DECIMALS = 4
DGS10_ALFRED_VINTAGE_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-29"

# These values were independently rechecked from the ALFRED CSV at the vintage URL
# above. The default is the original Project 2 input: the 2026-10-27 observation
# of 4.99%, available by the 2026-10-29 vintage.
DGS10_VERIFIED_RECORDS = (
    {
        "observation_date": date(2026, 10, 27),
        "available_on": date(2026, 10, 29),
        "value": 4.99,
        "evidence": "Verified directly from the ALFRED 2026-10-29 vintage CSV.",
    },
    {
        "observation_date": date(2026, 10, 26),
        "available_on": date(2026, 10, 29),
        "value": 5.00,
        "evidence": "Verified directly from the ALFRED 2026-10-29 vintage CSV.",
    },
    {
        "observation_date": date(2026, 10, 23),
        "available_on": date(2026, 10, 29),
        "value": 5.00,
        "evidence": "Verified directly from the ALFRED 2026-10-29 vintage CSV.",
    },
)


def _price_source_text(source):
    """Read a path or Streamlit upload without changing its contents."""
    if isinstance(source, (str, Path)):
        return Path(source).read_text(encoding="utf-8-sig")
    source.seek(0)
    raw = source.read()
    source.seek(0)
    return raw.decode("utf-8-sig") if isinstance(raw, bytes) else raw


def validate_price_csv(source, source_download_date=None):
    """Validate the required monthly price file and describe its observable coverage.

    This checks only what is present in the supplied CSV.  It intentionally does not
    manufacture prices or claim that a monthly label is a verified month-end close.
    """
    rows = list(csv.reader(_price_source_text(source).splitlines()))
    if not rows:
        raise ValueError("prices.csv is empty.")
    header = rows[0]
    expected_header = ["Date", *EXPECTED_TICKERS]
    if header != expected_header:
        raise ValueError(
            f"prices.csv must contain exactly these columns in this order: {', '.join(expected_header)}; "
            f"found: {', '.join(header) or '(no columns)'}"
        )

    parsed_dates = []
    for row_number, row in enumerate(rows[1:], start=2):
        if not row:
            continue
        if len(row) != len(expected_header):
            raise ValueError(f"prices.csv row {row_number} has {len(row)} columns; expected {len(expected_header)}.")
        try:
            observation_date = date.fromisoformat(row[0])
        except ValueError as error:
            raise ValueError(f"prices.csv row {row_number} has an invalid Date: {row[0]!r}.") from error
        if observation_date > date.today():
            raise ValueError(f"prices.csv row {row_number} is dated in the future: {observation_date.isoformat()}.")
        for ticker, raw_value in zip(EXPECTED_TICKERS, row[1:]):
            if raw_value.strip() == "":
                raise ValueError(f"prices.csv row {row_number}, {ticker} is missing.")
            try:
                value = float(raw_value)
            except ValueError as error:
                raise ValueError(f"prices.csv row {row_number}, {ticker} is not numeric: {raw_value!r}.") from error
            if not isfinite(value):
                raise ValueError(f"prices.csv row {row_number}, {ticker} must be finite.")
            if value <= 0:
                raise ValueError(f"prices.csv row {row_number}, {ticker} must be positive.")
        parsed_dates.append((row_number, observation_date))

    if len(parsed_dates) < 37:
        raise ValueError(
            "prices.csv needs at least 37 monthly prices (36 monthly returns) for the required 36-month stress test."
        )
    for (prior_row, prior), (current_row, current) in zip(parsed_dates, parsed_dates[1:]):
        if current <= prior:
            raise ValueError(
                f"prices.csv dates must be strictly chronological with no duplicates; rows {prior_row} and {current_row} are {prior} and {current}."
            )
        prior_month = prior.year * 12 + prior.month
        current_month = current.year * 12 + current.month
        if current_month != prior_month + 1:
            raise ValueError(
                f"prices.csv must have one observation per consecutive calendar month; rows {prior_row} and {current_row} skip from {prior} to {current}."
            )

    first_date = parsed_dates[0][1]
    last_date = parsed_dates[-1][1]
    partial_observation = False
    if source_download_date and (last_date.year, last_date.month) == (source_download_date.year, source_download_date.month):
        month_end = date(last_date.year, last_date.month, monthrange(last_date.year, last_date.month)[1])
        if source_download_date < month_end:
            partial_observation = True
            final_status = (
                f"Partial observation: the final {last_date:%Y-%m} monthly row was downloaded on "
                f"{source_download_date.isoformat()}, before that month ended on {month_end.isoformat()}. "
                "It remains in prices.csv unchanged; the app reports a separate exclusion sensitivity."
            )
        else:
            final_status = "The recorded download date is after the final observation month ended; completion is consistent with the date but the raw source timestamp is not retained."
    elif source_download_date is None:
        final_status = (
            "The replacement CSV has no recorded download date, so the app cannot independently determine whether its final monthly observation is complete."
        )
    else:
        today = date.today()
        if (last_date.year, last_date.month) < (today.year, today.month):
            final_status = (
                "The final monthly label precedes the current calendar month, but no matching source download date was supplied to independently prove month completion."
            )
        else:
            final_status = (
                "The final monthly label is in the current calendar month and may be partial; no matching source download date was supplied."
            )
    return {
        "tickers": EXPECTED_TICKERS,
        "observations": len(parsed_dates),
        "monthly_returns": len(parsed_dates) - 1,
        "first_date": first_date,
        "last_date": last_date,
        "partial_final_observation": partial_observation,
        "final_observation_status": final_status,
    }


def source_without_final_observation(source):
    """Return an in-memory sensitivity source with the final row removed, never editing the CSV."""
    rows = list(csv.reader(_price_source_text(source).splitlines()))
    nonempty_rows = [row for row in rows if row]
    if len(nonempty_rows) < 3:
        raise ValueError("Cannot exclude the final observation because fewer than two price rows remain.")
    output = StringIO()
    csv.writer(output, lineterminator="\n").writerows(nonempty_rows[:-1])
    output.seek(0)
    return output


def dgs10_vintage_status(mode="verified", observation_date=None, value=None):
    """Classify DGS10 evidence without presenting manual inputs as vintage-verified."""
    if mode == "verified":
        record = DGS10_VERIFIED_RECORDS[0]
        return {
            "status": "verified",
            **record,
            "message": (
                f"Verified directly against the ALFRED vintage: DGS10 {record['value']:.2f}% for "
                f"{record['observation_date'].isoformat()}, available by {record['available_on'].isoformat()}. "
                f"Source: {DGS10_ALFRED_VINTAGE_URL}"
            ),
        }
    if mode == "unavailable":
        return {
            "status": "unavailable",
            "observation_date": None,
            "available_on": None,
            "value": None,
            "message": "No DGS10 vintage observation is available. Do not use a substitute as point-in-time evidence.",
        }
    if observation_date is None or value is None or not isfinite(float(value)):
        return {
            "status": "unavailable",
            "observation_date": None,
            "available_on": None,
            "value": None,
            "message": "The manual DGS10 observation is incomplete or nonfinite and is unavailable for verification.",
        }
    return {
        "status": "unverified",
        "observation_date": observation_date,
        "available_on": None,
        "value": float(value),
        "message": "Manual DGS10 input is unverified: no ALFRED vintage evidence was supplied. It is not used as verified point-in-time evidence.",
    }


def apply_annual_cost(sleeves, annual_cost):
    """Apply an illustrative annual cost overlay to gross estimated returns only."""
    if not isfinite(annual_cost) or annual_cost < 0:
        raise ValueError("Annual investment cost must be a finite nonnegative decimal.")
    net_sleeves = {}
    for name, inputs in sleeves.items():
        net_sleeves[name] = dict(inputs)
        net_sleeves[name]["expected_return"] = inputs["expected_return"] - annual_cost
    return net_sleeves


def evaluate(weights, sleeves, correlations, reserve_eligible):
    """Return risk, return, reserve weight, and weights for any transparent allocation."""
    names = sleeve_names(sleeves)
    covariance = covariance_matrix(names, sleeves, correlations)
    return {
        "weights": weights,
        "expected_return": portfolio_return(weights, sleeves),
        "volatility": portfolio_volatility(weights, names, covariance),
        "reserve_eligible_weight": reserve_eligible_weight(weights, reserve_eligible),
    }


def verdict(result, objective, reserve_minimum):
    """Return PASS or FAIL plus the active rules that failed."""
    if result is None:
        return "FAIL", ["feasibility"]
    failed = []
    if result["expected_return"] < objective:
        failed.append("return objective")
    if result["reserve_eligible_weight"] < reserve_minimum:
        failed.append("reserve minimum")
    if abs(sum(result["weights"].values()) - 1) > 1e-12:
        failed.append("full investment")
    if any(weight < 0 for weight in result["weights"].values()):
        failed.append("long-only")
    return ("PASS", []) if not failed else ("FAIL", failed)


def largest_weight_change(left, right):
    """Return maximum absolute allocation change in percentage points."""
    if left is None or right is None:
        return None
    return max(abs(left["weights"][name] - right["weights"][name]) for name in left["weights"]) * 100


def format_weights(weights, names, decimals=1):
    """Render computed weights for display without introducing hardcoded allocations."""
    return " / ".join(f"{name} {weights[name] * 100:.{decimals}f}%" for name in names)


def endpoint_passes_both_windows(weights, results):
    """Test a displayed allocation using the unrounded engine under both return windows."""
    outcomes = []
    for sleeves, correlations in (
        (results["all_sleeves"], results["all_correlations"]),
        (results["stress_sleeves"], results["stress_correlations"]),
    ):
        outcomes.append(
            verdict(
                evaluate(weights, sleeves, correlations, results["reserve_eligible"]),
                results["objective"],
                results["reserve_minimum"],
            )[0] == "PASS"
        )
    return all(outcomes), outcomes


def conservative_executable_weights(weights, results, decimals=EXECUTABLE_WEIGHT_DECIMALS):
    """Find a nearby decimal-grid allocation that is executable and passes both windows.

    Displaying ordinary rounded weights can round an endpoint through its return boundary.
    This searches nearby 0.0001-percentage-point allocations, keeps only allocations
    that pass with unrounded arithmetic, and returns the closest safe display vector.
    """
    names = results["names"]
    units_per_percent = 10**decimals
    total_units = 100 * units_per_percent
    target_units = [weights[name] * 100 * units_per_percent for name in names]
    candidate_ranges = [
        range(max(0, floor(value) - 5), floor(value) + 6)
        for value in target_units[:-1]
    ]
    candidates = []
    for prefix in product(*candidate_ranges):
        final_unit = total_units - sum(prefix)
        if final_unit < 0:
            continue
        units = (*prefix, final_unit)
        candidate = {name: unit / (100 * units_per_percent) for name, unit in zip(names, units)}
        passes, outcomes = endpoint_passes_both_windows(candidate, results)
        if passes:
            distance = sum(abs(candidate[name] - weights[name]) for name in names)
            candidates.append((distance, candidate, outcomes))
    if not candidates:
        return None
    _, candidate, outcomes = min(candidates, key=lambda item: item[0])
    return {"weights": candidate, "decimals": decimals, "window_passes": outcomes}


def reaches_stability_threshold(change):
    """Treat numerical noise at the 25-point boundary as reaching the stop threshold."""
    return change is not None and change >= STABILITY_THRESHOLD_POINTS - STABILITY_COMPARISON_TOLERANCE_POINTS


def meridian_benchmark_weights(names):
    """Return Meridian's 60% VT / 40% LQD comparison benchmark when available."""
    if "VT" not in names or "LQD" not in names:
        return None
    weights = {name: 0.0 for name in names}
    weights["VT"] = 0.60
    weights["LQD"] = 0.40
    return weights


def original_mandate_status(results):
    """Classify the original Meridian requirements without inventing unavailable data."""
    base = results["base"]
    original_reserve = (
        "not available because the model has no feasible base allocation"
        if base is None
        else ("pass" if base["reserve_eligible_weight"] >= ORIGINAL_RESERVE_MINIMUM else "fail")
    )
    long_only = (
        "not available because the model has no feasible base allocation"
        if base is None
        else ("pass" if all(weight >= 0 for weight in base["weights"].values()) else "fail")
    )
    return [
        ("Original return objective", "Unverified", "CPI + 4% net of costs over rolling five-year periods is not tested. The current 6.5% target is a simplified historical estimate, not a guarantee."),
        ("Seven-year horizon and annual rebalancing", "Process requirement", "The app does not simulate seven years or perform/measure annual rebalancing."),
        ("Quarterly $750,000 payouts", "Unverified", "The cash-flow schedule and portfolio value are not modeled."),
        ("Minimum 3% reserve", "Computationally checked", original_reserve),
        ("Long-only", "Computationally checked", long_only),
        ("No borrowing or short sales", "Supported by model design", "The search uses nonnegative, fully invested weights; actual account borrowing/shorting is outside the supplied data."),
        ("No derivatives", "Unverified", "Fund holdings and implementation instruments are not supplied."),
        ("90% redeemable within five business days", "Unverified", "No redemption-terms or liquidity data are supplied."),
        ("8% maximum single-company exposure", "Unverified", "No look-through issuer holdings are supplied for the funds."),
        ("25% annual turnover without committee approval", "Unverified", "No prior holdings, trades, or rebalancing dates are supplied."),
        ("10% calendar-year loss provision", "Requires CIO clarification", "The loss measure, measurement period, and breach response are undefined."),
        ("Fund-universe support", "Supported by universe", "BIL and IEF are treated as reserve-eligible inputs; this does not verify fund liquidity, derivatives, or issuer look-through."),
    ]


def implementation_blockers(results):
    """Return original-mandate requirements that this model cannot fully clear."""
    blocking_statuses = {"Unverified", "Process requirement", "Requires CIO clarification"}
    return [
        requirement
        for requirement, status, _ in results["original_mandate_status"]
        if status in blocking_statuses
    ]


def blended_weights(base_weights, stress_weights, blend):
    """Return the unrounded common blend from base (0) to stress (1) weights."""
    return {
        name: (1 - blend) * base_weights[name] + blend * stress_weights[name]
        for name in base_weights
    }


def constraint_safe_range(results):
    """Return the full base-to-stress blend interval that passes under both windows.

    A portfolio chosen from a range must satisfy the active constraints not only under the
    window that produced one endpoint, but under both the full-history and 36-month return
    estimates. Return and reserve weights are linear in the blend, so solving their linear
    inequalities yields an interval whose every unrounded blend is mandate-compliant.
    """
    base = results["base"]
    stress = results["stress"]
    if base is None or stress is None:
        return None

    low, high = 0.0, 1.0
    environments = (
        (results["all_sleeves"], results["all_correlations"]),
        (results["stress_sleeves"], results["stress_correlations"]),
    )
    for sleeves, _ in environments:
        base_return = portfolio_return(base["weights"], sleeves)
        stress_return = portfolio_return(stress["weights"], sleeves)
        slope = stress_return - base_return
        required = results["objective"]
        if abs(slope) < 1e-15:
            if base_return < required:
                return None
        elif slope > 0:
            low = max(low, (required - base_return) / slope)
        else:
            high = min(high, (required - base_return) / slope)

    base_reserve = reserve_eligible_weight(base["weights"], results["reserve_eligible"])
    stress_reserve = reserve_eligible_weight(stress["weights"], results["reserve_eligible"])
    reserve_slope = stress_reserve - base_reserve
    if abs(reserve_slope) < 1e-15:
        if base_reserve < results["reserve_minimum"]:
            return None
    elif reserve_slope > 0:
        low = max(low, (results["reserve_minimum"] - base_reserve) / reserve_slope)
    else:
        high = min(high, (results["reserve_minimum"] - base_reserve) / reserve_slope)

    low, high = max(0.0, low), min(1.0, high)
    if low > high + 1e-12:
        return None

    lower_weights = blended_weights(base["weights"], stress["weights"], low)
    upper_weights = blended_weights(base["weights"], stress["weights"], high)
    for weights in (lower_weights, upper_weights):
        for sleeves, correlations in environments:
            state, _ = verdict(
                evaluate(weights, sleeves, correlations, results["reserve_eligible"]),
                results["objective"],
                results["reserve_minimum"],
            )
            if state != "PASS":
                return None
    lower_executable = conservative_executable_weights(lower_weights, results)
    upper_executable = conservative_executable_weights(upper_weights, results)
    if lower_executable is None or upper_executable is None:
        return None
    return {
        "lower_weights": lower_weights,
        "upper_weights": upper_weights,
        "lower_executable": lower_executable,
        "upper_executable": upper_executable,
        "lower_blend": low,
        "upper_blend": high,
        "names": results["names"],
        "rule": "The displayed endpoints are conservative executable allocations at 0.0001 percentage-point precision. Each is retested with unrounded arithmetic under both estimation windows; do not round them to fewer decimals.",
    }


def recommendation(results):
    """Turn calculated base/stress results into one transparent committee recommendation."""
    objective = results["objective"]
    reserve_minimum = results["reserve_minimum"]
    base = results["base"]
    stress = results["stress"]
    base_state, base_failures = verdict(base, objective, reserve_minimum)
    stress_state, stress_failures = verdict(stress, objective, reserve_minimum)

    if base_state != "PASS":
        detail = "no feasible base portfolio" if base is None else ", ".join(base_failures)
        return {
            "action": "Reject",
            "full_adoption_allowed": False,
            "reason": f"Reject the process because the base allocation fails: {detail}.",
            "allocation_range": None,
        }
    if stress_state != "PASS":
        detail = "no feasible stress portfolio" if stress is None else ", ".join(stress_failures)
        return {
            "action": "Stop",
            "full_adoption_allowed": False,
            "reason": f"Stop the process because the stress allocation fails: {detail}.",
            "allocation_range": None,
        }

    vintage = results.get("dgs10_vintage", {"status": "unavailable", "message": "No DGS10 status supplied."})
    if vintage["status"] != "verified":
        return {
            "action": "Stop",
            "full_adoption_allowed": False,
            "reason": (
                "Stop implementation pending DGS10 point-in-time review: "
                f"{vintage['message']}"
            ),
            "allocation_range": None,
        }

    change = results["largest_change"]
    allocation_range = constraint_safe_range(results)
    if allocation_range is None:
        return {
            "action": "Stop",
            "full_adoption_allowed": False,
            "reason": "Stop the process because no common allocation range passes the active mandate under both the base and stress estimation windows.",
            "allocation_range": None,
        }
    if reaches_stability_threshold(change):
        return {
            "action": "Pilot",
            "full_adoption_allowed": False,
            "reason": (
                f"Do not fully adopt: the calculated base-to-stress allocation change is {change:.2f} percentage points, "
                f"at or above the {STABILITY_THRESHOLD_POINTS:.0f}-point stability threshold."
            ),
            "allocation_range": allocation_range,
        }
    blockers = implementation_blockers(results)
    if blockers:
        return {
            "action": "Model approval only",
            "full_adoption_allowed": False,
            "reason": (
                f"The calculated stress movement is {change:.2f} percentage points, below the "
                f"{STABILITY_THRESHOLD_POINTS:.0f}-point stability threshold, but implementation approval is not allowed "
                f"until these original-mandate requirements are verified or resolved: {', '.join(blockers)}."
            ),
            "allocation_range": allocation_range,
        }
    return {
        "action": "Adopt",
        "full_adoption_allowed": True,
        "reason": (
            f"The calculated stress movement is {change:.2f} percentage points, below the "
            f"{STABILITY_THRESHOLD_POINTS:.0f}-point stability threshold and no remaining implementation blockers are recorded."
        ),
        "allocation_range": allocation_range,
    }


def build_project2_results(
    objective=OBJECTIVE,
    reserve_minimum=RESERVE_MINIMUM,
    source=None,
    annual_cost=0.0,
    dgs10_vintage=None,
    exclude_final_observation=False,
):
    """Compute baselines, constrained allocations, and stress results for active inputs."""
    using_default_source = source is None
    source = str(PRICES) if using_default_source else source
    if not isfinite(objective):
        raise ValueError("Objective must be finite.")
    if not isfinite(reserve_minimum) or reserve_minimum < 0 or reserve_minimum > 1:
        raise ValueError("Reserve minimum must be a finite value from 0% through 100%.")
    source_download_date = PRICE_DOWNLOAD_DATE if using_default_source else None
    source_price_validation = validate_price_csv(source, source_download_date)
    estimation_source = source_without_final_observation(source) if exclude_final_observation else source
    price_validation = validate_price_csv(estimation_source, source_download_date)
    gross_all_sleeves, all_correlations = estimate_from_csv(estimation_source, last_36_months=False)
    gross_stress_sleeves, stress_correlations = estimate_from_csv(estimation_source, last_36_months=True)
    all_sleeves = apply_annual_cost(gross_all_sleeves, annual_cost)
    stress_sleeves = apply_annual_cost(gross_stress_sleeves, annual_cost)
    names = sleeve_names(all_sleeves)
    reserve_eligible = {name for name in names if name in RESERVE_ELIGIBLE}
    equal = evaluate(equal_weight_portfolio(names), all_sleeves, all_correlations, reserve_eligible)
    inverse = evaluate(inverse_volatility_portfolio(names, all_sleeves), all_sleeves, all_correlations, reserve_eligible)
    benchmark_weights = meridian_benchmark_weights(names)
    benchmark = (
        evaluate(benchmark_weights, all_sleeves, all_correlations, reserve_eligible)
        if benchmark_weights is not None
        else None
    )
    base = search_lowest_risk_mix(all_sleeves, all_correlations, objective, reserve_eligible, reserve_minimum)
    stress = search_lowest_risk_mix(stress_sleeves, stress_correlations, objective, reserve_eligible, reserve_minimum)
    results = {
        "names": names,
        "objective": objective,
        "reserve_minimum": reserve_minimum,
        "reserve_eligible": reserve_eligible,
        "annual_cost": annual_cost,
        "price_validation": price_validation,
        "source_price_validation": source_price_validation,
        "excluded_final_observation": exclude_final_observation,
        "gross_all_sleeves": gross_all_sleeves,
        "gross_stress_sleeves": gross_stress_sleeves,
        "all_sleeves": all_sleeves,
        "all_correlations": all_correlations,
        "stress_sleeves": stress_sleeves,
        "stress_correlations": stress_correlations,
        "equal": equal,
        "inverse": inverse,
        "benchmark": benchmark,
        "base": base,
        "stress": stress,
        "largest_change": largest_weight_change(base, stress),
        "dgs10_vintage": dgs10_vintage or dgs10_vintage_status(),
    }
    results["original_mandate_status"] = original_mandate_status(results)
    results["recommendation"] = recommendation(results)
    return results


def final_observation_sensitivity(
    objective=OBJECTIVE,
    reserve_minimum=RESERVE_MINIMUM,
    source=None,
    annual_cost=0.0,
    dgs10_vintage=None,
):
    """Recompute from an in-memory copy without the final price row; never alter prices.csv."""
    results = build_project2_results(
        objective=objective,
        reserve_minimum=reserve_minimum,
        source=source,
        annual_cost=annual_cost,
        dgs10_vintage=dgs10_vintage,
        exclude_final_observation=True,
    )
    return {
        "excluded_date": results["source_price_validation"]["last_date"],
        "remaining_period": results["price_validation"],
        "base": results["base"],
        "stress": results["stress"],
        "largest_change": results["largest_change"],
        "recommendation": results["recommendation"],
        "names": results["names"],
    }


def cost_sensitivity(objective=OBJECTIVE, reserve_minimum=RESERVE_MINIMUM, source=None, dgs10_vintage=None):
    """Run the required illustrative annual-cost cases using the same net-return engine."""
    rows = []
    for basis_points in (0, 10, 25, 50):
        results = build_project2_results(
            objective=objective,
            reserve_minimum=reserve_minimum,
            source=source,
            annual_cost=basis_points / 10_000,
            dgs10_vintage=dgs10_vintage,
        )
        base = results["base"]
        state, failures = verdict(base, objective, reserve_minimum)
        rows.append({
            "cost_bps": basis_points,
            "base_verdict": state,
            "base_return": None if base is None else base["expected_return"],
            "base_volatility": None if base is None else base["volatility"],
            "base_reserve": None if base is None else base["reserve_eligible_weight"],
            "base_weights": None if base is None else base["weights"],
            "stress_weights": None if results["stress"] is None else results["stress"]["weights"],
            "largest_change": results["largest_change"],
            "failures": failures,
            "recommendation": results["recommendation"]["action"],
        })
    return rows


def report_section(label, result, results):
    """Render one result safely, including infeasible portfolios."""
    state, failures = verdict(result, results["objective"], results["reserve_minimum"])
    lines = [f"## {label}"]
    if result is None:
        lines.extend(["No feasible allocation.", f"Mandate verdict: {state} — failed: {', '.join(failures)}", ""])
        return lines
    lines.extend([
        f"Weights: {format_weights(result['weights'], results['names'])}",
        f"Expected return: {result['expected_return'] * 100:.2f}%",
        f"Volatility: {result['volatility'] * 100:.2f}%",
        f"Reserve-eligible: {result['reserve_eligible_weight'] * 100:.1f}%",
        f"Mandate verdict: {state}" + ("" if not failures else f" — failed: {', '.join(failures)}"),
        "",
    ])
    return lines


def render_recommendation(recommendation_data):
    """Render only calculated recommendation information for the text report."""
    lines = [f"Recommendation: {recommendation_data['action']}", recommendation_data["reason"]]
    allocation_range = recommendation_data["allocation_range"]
    if allocation_range is None:
        return lines
    names = allocation_range["names"]
    lines.extend([
        "Constraint-safe allocation range endpoints:",
        f"Lower executable endpoint (stress blend {allocation_range['lower_blend'] * 100:.2f}%): {format_weights(allocation_range['lower_executable']['weights'], names, allocation_range['lower_executable']['decimals'])}",
        f"Upper executable endpoint (stress blend {allocation_range['upper_blend'] * 100:.2f}%): {format_weights(allocation_range['upper_executable']['weights'], names, allocation_range['upper_executable']['decimals'])}",
        f"Endpoint verification (all months / last 36): lower {allocation_range['lower_executable']['window_passes']}; upper {allocation_range['upper_executable']['window_passes']}.",
        allocation_range["rule"],
    ])
    return lines


def render_report(results):
    """Render a deterministic, GitHub-readable report without importing Streamlit."""
    lines = [
        "# Project 2 visible executed output",
        "",
        "As-of price download: 2026-10-22. DGS10 data-card download: 2026-10-29.",
        f"Objective: {results['objective'] * 100:.2f}% estimated annual net return. "
        f"Reserve minimum: {results['reserve_minimum'] * 100:.1f}% in BIL + IEF.",
        f"Illustrative annual cost overlay: {results['annual_cost'] * 10_000:.0f} basis points. "
        "Gross historical estimates are reduced by this overlay; it is not a verified fund-cost record.",
        (
            f"Validated price coverage: {results['price_validation']['first_date'].isoformat()} through "
            f"{results['price_validation']['last_date'].isoformat()} "
            f"({results['price_validation']['observations']} observations; "
            f"{results['price_validation']['monthly_returns']} monthly returns)."
        ),
        f"DGS10 vintage status: {results['dgs10_vintage']['status']}. {results['dgs10_vintage']['message']}",
        "",
    ]
    source_validation = results["source_price_validation"]
    if source_validation["partial_final_observation"]:
        lines.extend([
            "Partial-final-observation warning: the final monthly row is partial because its recorded download date preceded that month-end. prices.csv is retained unchanged; see the in-memory exclusion sensitivity below.",
            "",
        ])
    for label, result in (
        ("Equal weight", results["equal"]),
        ("Inverse volatility", results["inverse"]),
        ("Meridian benchmark — 60% VT / 40% LQD", results["benchmark"]),
        ("Constrained, all months", results["base"]),
        ("Constrained, last 36 monthly returns", results["stress"]),
    ):
        lines.extend(report_section(label, result, results))
    if results["largest_change"] is None:
        lines.append("Largest base-to-stress allocation change: unavailable because a result is infeasible.")
    else:
        lines.append(f"Largest base-to-stress allocation change: {results['largest_change']:.2f} percentage points.")
    lines.append(f"Stop condition: {STABILITY_THRESHOLD_POINTS:.0f} percentage points or more, or no feasible stress allocation.")
    lines.append("The 25-point stability threshold is a model-sensitivity control, not the original 25% annual-turnover restriction.")
    lines.append("Original Meridian mandate: the 6.5% target is a simplified modeling assumption; it does not verify CPI + 4% net of costs over rolling five-year periods.")
    lines.extend(render_recommendation(results["recommendation"]))
    lines.extend(["", "## Illustrative annual-cost sensitivity"])
    for row in cost_sensitivity(
        objective=results["objective"],
        reserve_minimum=results["reserve_minimum"],
        dgs10_vintage=results["dgs10_vintage"],
    ):
        if row["base_weights"] is None or row["stress_weights"] is None:
            lines.append(f"{row['cost_bps']} bp: infeasible base or stress allocation; recommendation {row['recommendation']}.")
        else:
            lines.append(
                f"{row['cost_bps']} bp: base {format_weights(row['base_weights'], results['names'])}; "
                f"stress {format_weights(row['stress_weights'], results['names'])}; "
                f"movement {row['largest_change']:.2f} points; recommendation {row['recommendation']}."
            )
    lines.extend([
        "Costs are illustrative overlays, not verified fund-cost records; adjusted prices may already reflect fund expenses.",
        "",
        "## Partial-final-observation sensitivity",
    ])
    partial = final_observation_sensitivity(
        objective=results["objective"],
        reserve_minimum=results["reserve_minimum"],
        annual_cost=results["annual_cost"],
        dgs10_vintage=results["dgs10_vintage"],
    )
    lines.append(
        f"Excluded {partial['excluded_date'].isoformat()} in memory only; prices.csv is unchanged. "
        f"Remaining coverage: {partial['remaining_period']['first_date'].isoformat()} through "
        f"{partial['remaining_period']['last_date'].isoformat()} ({partial['remaining_period']['monthly_returns']} returns)."
    )
    if partial["base"] is None or partial["stress"] is None:
        lines.append("Partial-month sensitivity: a base or stress allocation is infeasible.")
    else:
        lines.extend(report_section("Partial sensitivity, all remaining months", partial["base"], {
            **results,
            "names": partial["names"],
        }))
        lines.extend(report_section("Partial sensitivity, last 36 remaining returns", partial["stress"], {
            **results,
            "names": partial["names"],
        }))
        lines.append(f"Partial sensitivity movement: {partial['largest_change']:.2f} percentage points.")
        lines.append(f"Partial sensitivity recommendation: {partial['recommendation']['action']}. {partial['recommendation']['reason']}")
    return "\n".join(lines)
