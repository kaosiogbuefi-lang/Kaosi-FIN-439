"""Lab 15 Streamlit interface for the portfolio stability decision.

Run with: streamlit run app.py
"""

from copy import deepcopy

import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    estimate_from_csv,
    search_lowest_risk_mix,
)


def display_result(label, result, names):
    """Display one optimizer result using the engine's calculated values."""
    st.subheader(label)
    if result is None:
        st.warning("No mix meets the objective and reserve rule.")
        return
    st.write("Weights")
    st.code(" / ".join(f"{name}: {result['weights'][name] * 100:.1f}%" for name in names))
    st.dataframe(
        {
            "Asset": names,
            "Weight (%)": [round(result["weights"][name] * 100, 1) for name in names],
        },
        hide_index=True,
        use_container_width=True,
    )
    left, right = st.columns(2)
    left.metric("Expected return", f"{result['expected_return'] * 100:.2f}%")
    right.metric("Volatility", f"{result['volatility'] * 100:.2f}%")
    st.metric("Reserve-eligible weight", f"{result['reserve_eligible_weight'] * 100:.1f}%")


def largest_weight_change(first, second, names):
    """Return the largest absolute change in weights, in percentage points."""
    if first is None or second is None:
        return None
    return max(abs(first["weights"][name] - second["weights"][name]) for name in names) * 100


st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

st.sidebar.header("Mandate and data")
objective = st.sidebar.number_input(
    "Objective return (%)", min_value=0.0, max_value=100.0,
    value=OBJECTIVE_RETURN * 100, step=0.1,
)
reserve_minimum = st.sidebar.number_input(
    "Minimum reserve-eligible weight (%)", min_value=0.0, max_value=100.0,
    value=3.0, step=1.0,
)
uploaded_file = st.sidebar.file_uploader("Upload monthly prices.csv", type="csv")
last_36_months = st.sidebar.toggle("Use only the last 36 monthly returns", value=False)

try:
    if uploaded_file is None:
        loaded_sleeves = deepcopy(SLEEVES)
        loaded_correlations = deepcopy(CORRELATIONS)
        data_label = "Meridian inputs"
    else:
        loaded_sleeves, loaded_correlations = estimate_from_csv(uploaded_file, last_36_months)
        data_label = "Uploaded CSV, last 36 monthly returns" if last_36_months else "Uploaded CSV, all months"
except (ValueError, UnicodeDecodeError) as error:
    st.error(f"Could not estimate from the CSV: {error}")
    st.stop()

st.caption(f"Loaded data: {data_label}. Returns are historical annualized estimates, not forecasts.")
names = list(loaded_sleeves)

st.header("Editable expected returns and reserve eligibility")
edited_sleeves = deepcopy(loaded_sleeves)
reserve_eligible = set()
for name in names:
    first, second = st.columns([3, 2])
    edited_sleeves[name]["expected_return"] = first.number_input(
        f"{name} expected return (%)", min_value=-100.0, max_value=100.0,
        value=float(loaded_sleeves[name]["expected_return"] * 100), step=0.1,
        key=f"return_{name}",
    ) / 100
    if second.checkbox(
        f"{name} is reserve-eligible",
        value=name in RESERVE_ELIGIBLE,
        key=f"reserve_{name}",
    ):
        reserve_eligible.add(name)

try:
    loaded_answer = search_lowest_risk_mix(
        loaded_sleeves, loaded_correlations, objective / 100, reserve_eligible, reserve_minimum / 100
    )
    edited_answer = search_lowest_risk_mix(
        edited_sleeves, loaded_correlations, objective / 100, reserve_eligible, reserve_minimum / 100
    )
except ValueError as error:
    st.error(f"Input error: {error}")
    st.stop()

st.header("Lowest-risk mix meeting the mandate")
as_loaded, current = st.columns(2)
with as_loaded:
    display_result("As loaded", loaded_answer, names)
with current:
    display_result("With edited returns", edited_answer, names)

change = largest_weight_change(loaded_answer, edited_answer, names)
if change is None:
    st.info("Largest weight change is unavailable because one result has no feasible mix.")
else:
    st.success(f"Largest weight change: {change:.0f} percentage points")
