"""Project 2 investment-management decision app.

Run from this folder with: streamlit run app.py
"""

from datetime import date

import streamlit as st

from app_logic import (
    OBJECTIVE,
    RESERVE_MINIMUM,
    STABILITY_THRESHOLD_POINTS,
    build_project2_results,
    cost_sensitivity,
    dgs10_vintage_status,
    final_observation_sensitivity,
    format_weights,
    original_mandate_status,
    reaches_stability_threshold,
    verdict,
)


def show_portfolio(label, result, results):
    """Show calculated weights, metrics, and active-mandate verdict safely."""
    st.subheader(label)
    state, failures = verdict(result, results["objective"], results["reserve_minimum"])
    if result is None:
        st.error("FAIL — no feasible allocation: " + ", ".join(failures))
        return
    names = results["names"]
    st.dataframe(
        {
            "Fund": names,
            "Weight (%)": [round(result["weights"][name] * 100, 1) for name in names],
        },
        hide_index=True,
        use_container_width=True,
    )
    left, middle, right = st.columns(3)
    left.metric("Expected return", f"{result['expected_return'] * 100:.2f}%")
    middle.metric("Volatility", f"{result['volatility'] * 100:.2f}%")
    right.metric("Reserve-eligible", f"{result['reserve_eligible_weight'] * 100:.1f}%")
    if state == "PASS":
        st.success("PASS — meets the model's return, reserve, long-only, and full-investment checks only.")
    else:
        st.error("FAIL — " + ", ".join(failures))


def show_recommendation(recommendation_data):
    """Display the one shared, dynamically calculated committee recommendation."""
    st.header("Committee recommendation")
    action = recommendation_data["action"]
    if action == "Adopt":
        st.success(f"{action}: {recommendation_data['reason']}")
    elif action in ("Pilot", "Model approval only"):
        st.warning(f"{action}: {recommendation_data['reason']}")
    else:
        st.error(f"{action}: {recommendation_data['reason']}")

    allocation_range = recommendation_data["allocation_range"]
    if allocation_range is None:
        return
    names = allocation_range["names"]
    st.write("**Conservative, executable allocation range**")
    lower = allocation_range["lower_executable"]
    upper = allocation_range["upper_executable"]
    st.write(
        f"Lower endpoint (stress blend {allocation_range['lower_blend'] * 100:.2f}%): "
        + format_weights(lower["weights"], names, lower["decimals"])
    )
    st.write(
        f"Upper endpoint (stress blend {allocation_range['upper_blend'] * 100:.2f}%): "
        + format_weights(upper["weights"], names, upper["decimals"])
    )
    st.caption(f"Endpoint verification (all months / last 36): lower {lower['window_passes']}; upper {upper['window_passes']}.")
    st.caption(allocation_range["rule"])


st.set_page_config(page_title="Project 2 — Portfolio Decision", layout="wide")
st.title("Project 2 — Portfolio Decision")
st.caption(
    "AI used: Codex helped implement and test this learning app. "
    "The analysis and decision are mine. Education, not investment advice."
)

st.sidebar.header("Mandate and estimates")
objective = st.sidebar.number_input("Objective return (%)", 0.0, 100.0, OBJECTIVE * 100, 0.1) / 100
reserve_minimum = st.sidebar.number_input("Minimum BIL + IEF reserve (%)", 0.0, 100.0, RESERVE_MINIMUM * 100, 0.5) / 100
annual_cost = st.sidebar.number_input(
    "Illustrative annual investment cost (basis points)", 0.0, 500.0, 0.0, 1.0,
) / 10_000
uploaded_file = st.sidebar.file_uploader("Optional replacement monthly prices.csv", type="csv")

st.sidebar.header("DGS10 point-in-time evidence")
dgs_mode = st.sidebar.selectbox(
    "Evidence status",
    ("Verified ALFRED vintage (2026-10-29)", "Manual observation (unverified)", "Unavailable"),
)
if dgs_mode == "Verified ALFRED vintage (2026-10-29)":
    dgs10_vintage = dgs10_vintage_status("verified")
elif dgs_mode == "Manual observation (unverified)":
    manual_date = st.sidebar.date_input("Manual DGS10 observation date", value=date(2026, 10, 29))
    manual_rate = st.sidebar.number_input("Manual DGS10 rate (%)", 0.0, 20.0, 4.99, 0.01)
    dgs10_vintage = dgs10_vintage_status("manual", manual_date, manual_rate)
else:
    dgs10_vintage = dgs10_vintage_status("unavailable")

try:
    results = build_project2_results(
        objective,
        reserve_minimum,
        uploaded_file,
        annual_cost=annual_cost,
        dgs10_vintage=dgs10_vintage,
    )
except (ValueError, UnicodeDecodeError) as error:
    st.error(f"Price-data error: {error}")
    st.stop()

st.header("Mandate")
st.write(
    "**Original objective:** CPI + 4% net of costs over rolling five-year periods. "
    f"**Current model target:** at least {objective * 100:.1f}% estimated annual return; this is a simplified modeling assumption, not a guarantee of the original objective. "
    f"**Universe:** BIL, IEF, LQD, and VT. **Hard constraint:** at least {reserve_minimum * 100:.1f}% in reserve-eligible BIL and IEF. "
    "**Risk measure:** annualized volatility from monthly adjusted-close returns. "
    "**Original benchmark:** 60% VT / 40% LQD."
)
st.caption("Returns are five-year historical annualized estimates, not forecasts. Prices are oldest-first monthly adjusted closes, downloaded 2026-10-22.")
st.write(
    f"**Return-cost treatment:** gross historical estimated returns are reduced by an illustrative annual cost overlay of "
    f"{annual_cost * 10_000:.0f} basis points before the mandate and recommendation are calculated. "
    "This is not a verified record of actual fund costs. Adjusted prices can already reflect fund-level expenses, so this overlay is a sensitivity test rather than an expense calculation."
)

st.header("Historical-price validation")
validation = results["price_validation"]
st.success(
    f"Validated exactly BIL, IEF, LQD, and VT: {validation['observations']} monthly observations from "
    f"{validation['first_date'].isoformat()} through {validation['last_date'].isoformat()} "
    f"({validation['monthly_returns']} monthly returns)."
)
st.caption(validation["final_observation_status"])
if results["source_price_validation"]["partial_final_observation"]:
    st.warning("The default final October 2026 row is partial because it was downloaded before October month-end. It remains in the base calculation; a non-destructive exclusion sensitivity appears below.")
gross_net_rows = []
for name in results["names"]:
    gross_net_rows.append({
        "Fund": name,
        "Gross historical estimated return (%)": round(results["gross_all_sleeves"][name]["expected_return"] * 100, 2),
        "Estimated net return after cost (%)": round(results["all_sleeves"][name]["expected_return"] * 100, 2),
    })
st.dataframe(gross_net_rows, hide_index=True, use_container_width=True)

left, second, third, right = st.columns(4)
with left:
    show_portfolio("Baseline 1 — Equal weight", results["equal"], results)
with second:
    show_portfolio("Baseline 2 — Inverse volatility", results["inverse"], results)
with third:
    show_portfolio("Original Meridian benchmark — 60% VT / 40% LQD", results["benchmark"], results)
with right:
    show_portfolio("Constrained lowest-risk portfolio", results["base"], results)

st.header("Original Meridian mandate: verification status")
st.write(
    "A passing model result is not full Meridian compliance. The table distinguishes checks computed from the available price data, "
    "requirements only supported by the chosen fund universe or model design, and requirements that cannot be verified without additional information."
)
status_rows = [
    {"Requirement": requirement, "Status": status, "Evidence or limitation": detail}
    for requirement, status, detail in original_mandate_status(results)
]
st.dataframe(status_rows, hide_index=True, use_container_width=True)

st.header("Point-in-time rate signal")
if dgs10_vintage["status"] == "verified":
    dgs10 = dgs10_vintage["value"]
    regime = "elevated-rate regime" if dgs10 >= 4.5 else "lower-rate regime"
    st.success(
        f"**Verified signal:** DGS10 was {dgs10:.2f}% on {dgs10_vintage['observation_date']:%Y-%m-%d}, "
        f"available by {dgs10_vintage['available_on']:%Y-%m-%d}; this is a {regime} under the 4.50% monitoring threshold."
    )
else:
    st.warning(f"**{dgs10_vintage['status'].title()} signal:** {dgs10_vintage['message']}")
st.caption(
    "Data card: DGS10 is the daily 10-year Treasury constant-maturity yield, percent and not seasonally adjusted, from FRED/ALFRED. "
    "The decision rule uses the ALFRED value available on the decision date; a current value published later is excluded. "
    "The signal is a monitor for IEF and LQD rate sensitivity, not a return forecast."
)

st.header("Stress run — estimation window")
stress_left, stress_right = st.columns(2)
with stress_left:
    show_portfolio("Base: all monthly observations", results["base"], results)
with stress_right:
    show_portfolio("Stress: only the last 36 monthly returns", results["stress"], results)
change = results["largest_change"]
if change is None:
    st.error("Stop condition met: a base or stress allocation is infeasible.")
elif reaches_stability_threshold(change):
    st.warning(f"Stop condition met: the largest allocation change is {change:.2f} percentage points (threshold: {STABILITY_THRESHOLD_POINTS:.0f}).")
else:
    st.success(f"Stress result: largest allocation change is {change:.2f} percentage points, below the {STABILITY_THRESHOLD_POINTS:.0f}-point stop threshold.")
st.caption(
    "The 25-percentage-point stability threshold is a model-sensitivity control. It is not the original mandate's "
    "25% annual turnover restriction, which cannot be verified without prior holdings and trade data."
)

st.header("Partial-final-observation sensitivity")
try:
    final_row_test = final_observation_sensitivity(
        objective=objective,
        reserve_minimum=reserve_minimum,
        source=uploaded_file,
        annual_cost=annual_cost,
        dgs10_vintage=dgs10_vintage,
    )
    st.write(
        f"This test excludes {final_row_test['excluded_date'].isoformat()} in memory only; prices.csv is unchanged. "
        f"Remaining estimation coverage: {final_row_test['remaining_period']['first_date'].isoformat()} through "
        f"{final_row_test['remaining_period']['last_date'].isoformat()} "
        f"({final_row_test['remaining_period']['monthly_returns']} monthly returns)."
    )
    if final_row_test["base"] is None or final_row_test["stress"] is None:
        st.warning("Excluding the final observation makes a base or stress allocation infeasible.")
    else:
        st.dataframe(
            [
                {"Run": "All remaining months", "Weights": format_weights(final_row_test["base"]["weights"], final_row_test["names"]), "Return (%)": round(final_row_test["base"]["expected_return"] * 100, 2), "Volatility (%)": round(final_row_test["base"]["volatility"] * 100, 2)},
                {"Run": "Last 36 remaining returns", "Weights": format_weights(final_row_test["stress"]["weights"], final_row_test["names"]), "Return (%)": round(final_row_test["stress"]["expected_return"] * 100, 2), "Volatility (%)": round(final_row_test["stress"]["volatility"] * 100, 2)},
            ],
            hide_index=True,
            use_container_width=True,
        )
        st.write(f"Largest movement after excluding the final observation: {final_row_test['largest_change']:.2f} percentage points. Recommendation: {final_row_test['recommendation']['action']}.")
except (ValueError, UnicodeDecodeError) as error:
    st.warning(f"Final-observation sensitivity unavailable: {error}")

st.header("Illustrative cost sensitivity")
try:
    sensitivity_rows = cost_sensitivity(
        objective=objective,
        reserve_minimum=reserve_minimum,
        source=uploaded_file,
        dgs10_vintage=dgs10_vintage,
    )
    st.dataframe(
        [
            {
                "Annual cost (bp)": row["cost_bps"],
                "Base verdict": row["base_verdict"],
                "Base net return (%)": None if row["base_return"] is None else round(row["base_return"] * 100, 2),
                "Base volatility (%)": None if row["base_volatility"] is None else round(row["base_volatility"] * 100, 2),
                "Reserve (%)": None if row["base_reserve"] is None else round(row["base_reserve"] * 100, 1),
                "Base weights": "infeasible" if row["base_weights"] is None else format_weights(row["base_weights"], results["names"]),
                "Stress weights": "infeasible" if row["stress_weights"] is None else format_weights(row["stress_weights"], results["names"]),
                "Base-to-stress movement (pp)": None if row["largest_change"] is None else round(row["largest_change"], 4),
                "Recommendation": row["recommendation"],
            }
            for row in sensitivity_rows
        ],
        hide_index=True,
        use_container_width=True,
    )
except (ValueError, UnicodeDecodeError) as error:
    st.error(f"Cost sensitivity could not be calculated: {error}")
st.caption("0, 10, 25, and 50 basis points are illustrative annual-cost assumptions only; they are not verified actual fund costs.")

show_recommendation(results["recommendation"])
