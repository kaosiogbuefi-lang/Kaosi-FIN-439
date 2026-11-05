"""Lab 19 Streamlit legend panel, powered by one deterministic EDGAR engine.

Run with: streamlit run buffett_app.py
"""

import re
from pathlib import Path

import streamlit as st

from buffett_10k import analyze_ticker, format_percent, format_percent_two_decimals, format_value, printed_number_tokens


INVESTORS = {
    "Buffett": ("checks", "buffett"),
    "Cathie Wood": ("cathie_checks", "cathie_wood"),
    "Burry": ("burry_checks", "burry"),
}


def memo_path(ticker, filename_part):
    """Return the memo file name written by the matching investor skill."""
    return Path(f"{ticker.upper()}_{filename_part}_memo.md")


def memo_number_flags(memo, allowed_tokens):
    """Return numeric tokens in a memo which the deterministic script did not print."""
    memo_tokens = set(re.findall(r"\b\d+(?:\.\d+)?%?", memo))
    return sorted(memo_tokens - allowed_tokens)


def display_rows(rows):
    """Render facts, code-computed values, and their XBRL tags."""
    display = []
    for row in rows:
        liabilities_ratio = (
            None
            if row["Liabilities"] is None or row["Equity"] in (None, 0)
            else row["Liabilities"] / row["Equity"]
        )
        display.append(
            {
                "Fiscal year end": row["Fiscal year end"],
                "Revenue ($m)": format_value(row["Revenue"]),
                "Revenue tag": row["tags"]["Revenue"],
                "Net income ($m)": format_value(row["Net income"]),
                "Operating cash flow ($m)": format_value(row["Operating cash flow"]),
                "Capital spending ($m)": format_value(row["Capital spending"]),
                "R&D ($m)": format_value(row["Research and development"]),
                "R&D tag": row["tags"]["Research and development"],
                "Equity ($m)": format_value(row["Equity"]),
                "Liabilities ($m)": format_value(row["Liabilities"]),
                "Liabilities / equity": "not known" if liabilities_ratio is None else f"{liabilities_ratio:.2f}",
                "ROE": format_percent(row["ROE"]),
                "Owner earnings ($m)": format_value(row["Owner earnings"]),
            }
        )
    st.dataframe(display, hide_index=True, use_container_width=True)


def panel_rows(analysis):
    """Make the investor-by-check panel directly from the three code check sets."""
    rows = []
    for investor, (check_key, _) in INVESTORS.items():
        for check, result in analysis[check_key].items():
            rows.append({"Investor": investor, "Check": check, "Result": result})
    return rows


st.set_page_config(page_title="Legend Panel", layout="wide")
st.title("Legend Panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.sidebar.text_input("Ticker", value="COST").strip().upper()
if not ticker:
    st.stop()

try:
    analysis = analyze_ticker(ticker)
except ValueError as error:
    st.error(str(error))
    st.stop()

st.subheader(f"{analysis['company']} ({analysis['ticker']})")
chart_rows = [
    {"Fiscal year end": row["Fiscal year end"], "Owner earnings": row["Owner earnings"], "Net income": row["Net income"]}
    for row in analysis["rows"]
]
st.line_chart(chart_rows, x="Fiscal year end", y=["Owner earnings", "Net income"], x_label="Fiscal year end", y_label="USD millions")
display_rows(analysis["rows"])

st.subheader("Panel checks")
st.dataframe(panel_rows(analysis), hide_index=True, use_container_width=True)
st.write(f"**Revenue growth a year, first year to last:** {format_percent_two_decimals(analysis['revenue_growth'])}")

st.subheader("Investor memos")
allowed = printed_number_tokens(analysis)
columns = st.columns(3)
for column, (investor, (_, filename_part)) in zip(columns, INVESTORS.items()):
    with column:
        st.markdown(f"### {investor}")
        path = memo_path(ticker, filename_part)
        if not path.exists():
            st.warning(f"No memo found at {path.name}. Run that skill and save its memo there.")
            continue
        memo = path.read_text(encoding="utf-8")
        st.markdown(memo)
        flags = memo_number_flags(memo, allowed)
        if flags:
            st.error("Unprinted number(s): " + ", ".join(flags))
        else:
            st.success("Every number was printed by the EDGAR script.")
