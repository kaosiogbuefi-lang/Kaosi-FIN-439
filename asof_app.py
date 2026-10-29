"""Lab 17 - a FRED-style point-in-time interest-rate app.

Run with: streamlit run asof_app.py
"""

import csv
import io
import re
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
FRED_GRAPH = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_GRAPH = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"


def series_url(series_id):
    """Return the public FRED page for one series."""
    return f"https://fred.stlouisfed.org/series/{series_id}"


def parse_fred_csv(csv_text, series_id):
    """Return usable date/value observations from a FRED or ALFRED CSV response."""
    reader = csv.DictReader(io.StringIO(csv_text))
    if not reader.fieldnames or len(reader.fieldnames) < 2:
        raise ValueError("The download did not contain a date and value column.")
    date_column = reader.fieldnames[0]
    value_column = next(
        (column for column in reader.fieldnames[1:] if column.upper() == series_id.upper()),
        reader.fieldnames[1],
    )
    observations = []
    for row in reader:
        raw_value = (row.get(value_column) or "").strip()
        if raw_value in ("", "."):
            continue
        try:
            observations.append({"Date": date.fromisoformat(row[date_column]), "Value": float(raw_value)})
        except (TypeError, ValueError):
            continue
    if not observations:
        raise ValueError(f"No numeric observations were returned for {series_id}.")
    return observations


def download_csv(base_url, parameters, series_id):
    """Download one public CSV and parse it without requiring an API key."""
    request_url = f"{base_url}?{urlencode(parameters)}"
    request = Request(request_url, headers={"User-Agent": "Lab-17-learning-app/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            csv_text = response.read().decode("utf-8-sig")
    except HTTPError as error:
        raise ValueError(f"FRED returned HTTP {error.code} for {series_id}.") from error
    except URLError as error:
        raise ValueError(f"Could not reach FRED for {series_id}: {error.reason}") from error
    return parse_fred_csv(csv_text, series_id)


@st.cache_data(show_spinner=False)
def download_today(series_id):
    """Download the values FRED displays today for one series."""
    return download_csv(FRED_GRAPH, {"id": series_id}, series_id)


@st.cache_data(show_spinner=False)
def download_as_known_on(series_id, vintage_date):
    """Download the values ALFRED displayed as of vintage_date."""
    return download_csv(
        ALFRED_GRAPH,
        {"id": series_id, "vintage_date": vintage_date.isoformat()},
        series_id,
    )


def last_observation(observations):
    """Return the last observation in a chronological list."""
    return max(observations, key=lambda observation: observation["Date"])


def after_start(observations, start_date):
    """Return observations measured on or after the selected chart start date."""
    return [observation for observation in observations if observation["Date"] >= start_date]


def revision_counts(today, vintage):
    """Count unavailable-later values and changed values on common observation dates."""
    today_by_date = {observation["Date"]: observation["Value"] for observation in today}
    vintage_by_date = {observation["Date"]: observation["Value"] for observation in vintage}
    vintage_last_date = last_observation(vintage)["Date"]
    later_count = sum(observation_date > vintage_last_date for observation_date in today_by_date)
    revised_count = sum(
        abs(today_by_date[observation_date] - vintage_value) > 1e-12
        for observation_date, vintage_value in vintage_by_date.items()
        if observation_date in today_by_date
    )
    return later_count, revised_count


def format_date(value):
    """Format a measured date for a compact audit table."""
    return value.isoformat()


def show_audit_table(rows):
    """Render a Markdown table whose FRED-series IDs are direct source links."""
    st.subheader("Point-in-time audit")
    headers = [
        "Series",
        "Last date known then",
        "Value then",
        "Last date today",
        "Value today",
        "Values later than then",
        "Revised same-date values",
    ]
    table = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for row in rows:
        table.append(
            "| "
            + " | ".join(
                [
                    f"[{row['id']}]({series_url(row['id'])})",
                    format_date(row["known_date"]),
                    f"{row['known_value']:.2f}",
                    format_date(row["today_date"]),
                    f"{row['today_value']:.2f}",
                    str(row["later_count"]),
                    str(row["revised_count"]),
                ]
            )
            + " |"
        )
    st.markdown("\n".join(table))


st.set_page_config(page_title="Point-in-Time Rate Audit", layout="wide")
st.title("Point-in-Time Rate Audit")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded "
    f"{date.today().isoformat()}; built with AI help, a learning demonstration, not investment advice."
)

st.sidebar.header("Series and dates")
selected_ids = st.sidebar.multiselect(
    "FRED series",
    options=list(SERIES),
    default=list(SERIES),
    format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
)
extra_id = st.sidebar.text_input("Add another FRED series ID (for example, PAYEMS)").strip().upper()
if extra_id:
    if not re.fullmatch(r"[A-Z0-9_]+", extra_id):
        st.sidebar.error("Use only letters, numbers, and underscores in a FRED series ID.")
    elif extra_id not in selected_ids:
        selected_ids.append(extra_id)

start_date = st.sidebar.date_input("Chart start date", value=date(2020, 1, 1))
as_known_date = st.sidebar.date_input("As known on", value=date.today())

if not selected_ids:
    st.info("Select at least one series ID to begin the audit.")
    st.stop()

audit_rows = []
for series_id in selected_ids:
    try:
        today_observations = download_today(series_id)
        vintage_observations = download_as_known_on(series_id, as_known_date)
        chart_observations = after_start(today_observations, start_date)
        if not chart_observations:
            raise ValueError(f"No {series_id} observations exist on or after {start_date}.")
        known_last = last_observation(vintage_observations)
        today_last = last_observation(today_observations)
        later_count, revised_count = revision_counts(today_observations, vintage_observations)
    except ValueError as error:
        st.error(f"{series_id}: {error}")
        continue

    st.subheader(f"{series_id} — {SERIES.get(series_id, 'Added FRED series')}")
    st.line_chart(chart_observations, x="Date", y="Value", x_label="Date", y_label="Value")
    st.caption(
        f"Last date known on {as_known_date.isoformat()}: "
        f"{known_last['Date'].isoformat()} ({known_last['Value']:.2f})"
    )
    audit_rows.append(
        {
            "id": series_id,
            "known_date": known_last["Date"],
            "known_value": known_last["Value"],
            "today_date": today_last["Date"],
            "today_value": today_last["Value"],
            "later_count": later_count,
            "revised_count": revised_count,
        }
    )

if audit_rows:
    show_audit_table(audit_rows)
