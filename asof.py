"""Lab 16 - point-in-time provenance gate.

Run with: python asof.py
"""

from datetime import date


# Editable inputs
DECISION_DATE = date.fromisoformat("2026-03-31")

ROWS = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published": "2026-02-10", "price": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published": "2026-03-10", "price": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published": "2026-04-10", "price": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published": "2026-03-25", "price": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published": "2026-02-10", "price": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "price": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "price": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published": "2026-04-10", "price": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published": "2026-02-10", "price": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published": "2026-04-05", "price": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published": "2026-03-10", "price": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published": "2026-03-10", "price": 111.0},
]


def publication_date(row):
    """Return a row's publication date as a date object."""
    return date.fromisoformat(row["published"])


def split_missing_ticker(rows):
    """Return admitted rows and quarantined rows with no ticker."""
    admitted = [row for row in rows if row["ticker"].strip()]
    removed = [row for row in rows if not row["ticker"].strip()]
    return admitted, removed


def remove_exact_duplicates(rows):
    """Keep the first occurrence of each identical data record."""
    admitted = []
    removed = []
    seen = set()
    for row in rows:
        fingerprint = (row["ticker"], row["month"], row["published"], row["price"])
        if fingerprint in seen:
            removed.append(row)
        else:
            seen.add(fingerprint)
            admitted.append(row)
    return admitted, removed


def remove_after_decision_date(rows, decision_date):
    """Keep rows published on or before the decision date."""
    admitted = [row for row in rows if publication_date(row) <= decision_date]
    removed = [row for row in rows if publication_date(row) > decision_date]
    return admitted, removed


def keep_latest_vintage(rows):
    """For each ticker/month, keep its latest published row."""
    newest_by_series_month = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in newest_by_series_month or publication_date(row) > publication_date(
            newest_by_series_month[key]
        ):
            newest_by_series_month[key] = row
    admitted = [row for row in rows if newest_by_series_month[(row["ticker"], row["month"])] is row]
    removed = [row for row in rows if row not in admitted]
    return admitted, removed


def apply_provenance_gate(rows, decision_date):
    """Apply the four stated rules and return the panel plus funnel results."""
    rows, missing_ticker = split_missing_ticker(rows)
    rows, duplicates = remove_exact_duplicates(rows)
    rows, after_decision = remove_after_decision_date(rows, decision_date)
    panel, older_vintages = keep_latest_vintage(rows)
    funnel = [
        ("Quarantined: no ticker", missing_ticker),
        ("Exact duplicate", duplicates),
        (f"Published after {decision_date.isoformat()}", after_decision),
        ("Older vintage replaced by a revision", older_vintages),
    ]
    return panel, funnel


def naive_panel(rows):
    """Keep latest publications without applying a decision-date restriction."""
    rows, _ = split_missing_ticker(rows)
    rows, _ = remove_exact_duplicates(rows)
    panel, _ = keep_latest_vintage(rows)
    return panel


def percent_change_from_previous_month(panel):
    """Return each ticker's latest-month price change from its prior month."""
    by_ticker = {}
    for row in panel:
        by_ticker.setdefault(row["ticker"], []).append(row)
    signals = {}
    for ticker, ticker_rows in by_ticker.items():
        ticker_rows.sort(key=lambda row: row["month"])
        if len(ticker_rows) < 2:
            continue
        previous, latest = ticker_rows[-2:]
        signals[ticker] = {
            "month": latest["month"],
            "change": latest["price"] / previous["price"] - 1,
        }
    return signals


def row_numbers(rows):
    """Format original row numbers for transparent funnel output."""
    return ", ".join(str(row["row"]) for row in rows) or "none"


def print_funnel(funnel):
    """Print the count and original row numbers removed at each rule."""
    print("Row funnel")
    for label, removed in funnel:
        print(f"{label}: {len(removed)} removed (row(s): {row_numbers(removed)})")


def print_panel(panel):
    """Print the surviving as-of rows in original-row order."""
    print("\nAs-of panel")
    print("Row  Ticker  Month     Published   Price")
    for row in panel:
        print(f"{row['row']:>3}  {row['ticker']:<6}  {row['month']}  {row['published']}  {row['price']:.1f}")


def print_signals(label, panel):
    """Print one signal per ticker from a panel."""
    print(f"\n{label}")
    for ticker, signal in percent_change_from_previous_month(panel).items():
        print(f"{ticker}: {signal['change']:+.2%} ({signal['month']})")


def main():
    """Run the point-in-time and naive comparisons from the editable inputs."""
    panel, funnel = apply_provenance_gate(ROWS, DECISION_DATE)
    print_funnel(funnel)
    print_panel(panel)
    print_signals("As-of signals", panel)
    print_signals("Naive signals (all latest publications)", naive_panel(ROWS))


if __name__ == "__main__":
    main()
