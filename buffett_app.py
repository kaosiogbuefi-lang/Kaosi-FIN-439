"""Lab 18 Streamlit app for a deterministic 10-K Buffett screen.

Run with: streamlit run buffett_app.py
"""

import re
from pathlib import Path

import streamlit as st

from buffett_10k import analyze_ticker, format_percent, format_value, printed_number_tokens


def memo_path(ticker):
    """Return the expected local memo path for a ticker."""
    return Path(f"{ticker.upper()}_buffett_memo.md")


def memo_number_flags(memo, allowed_tokens):
    """Return every distinct numeric token in a memo that code did not print."""
    memo_tokens = set(re.findall(r"\b\d+(?:\.\d+)?%?", memo))
    return sorted(memo_tokens - allowed_tokens)


def display_rows(rows):
    """Render a table with each computed value and its source XBRL tag."""
    display = []
    for row in rows:
        display.append(
            {
                "Fiscal year end": row["Fiscal year end"],
                "Revenue ($m)": format_value(row["Revenue"]),
                "Revenue tag": row["tags"]["Revenue"],
                "Net income ($m)": format_value(row["Net income"]),
                "Net income tag": row["tags"]["Net income"],
                "Operating cash flow ($m)": format_value(row["Operating cash flow"]),
                "Operating cash flow tag": row["tags"]["Operating cash flow"],
                "Capital spending ($m)": format_value(row["Capital spending"]),
                "Capital spending tag": row["tags"]["Capital spending"],
                "Equity ($m)": format_value(row["Equity"]),
                "Equity tag": row["tags"]["Equity"],
                "ROE": format_percent(row["ROE"]),
                "Owner earnings ($m)": format_value(row["Owner earnings"]),
            }
        )
    st.dataframe(display, hide_index=True, use_container_width=True)


st.set_page_config(page_title="Buffett 10-K Screen", layout="wide")
st.title("Buffett 10-K Screen")
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

st.subheader("Buffett checks")
for label, result in analysis["checks"].items():
    st.write(f"- **{label}:** {result}")

st.subheader("Buffett-style memo")
path = memo_path(ticker)
if not path.exists():
    st.warning(f"No memo found at {path.name}. Run the skill and save its memo there.")
else:
    memo = path.read_text(encoding="utf-8")
    st.markdown(memo)
    flags = memo_number_flags(memo, printed_number_tokens(analysis))
    if flags:
        st.error("Numbers in the memo not printed by the script: " + ", ".join(flags))
    else:
        st.success("Every number in this memo was printed by the EDGAR script.")
