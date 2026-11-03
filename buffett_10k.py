"""Deterministic 10-K facts and Buffett-style checks for Lab 18.

Run with: python buffett_10k.py COST
Uses Kaosi kogbuef@purdue.edu as its SEC User-Agent by default; SEC_USER_AGENT can override it.
"""

import json
import os
import re
import sys
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
USER_AGENT = os.environ.get("SEC_USER_AGENT", "Kaosi kogbuef@purdue.edu")
FLOW_METRICS = {
    "Revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "Net income": ["NetIncomeLoss"],
    "Operating cash flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "Capital spending": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],
}
POINT_METRICS = {"Equity": ["StockholdersEquity"]}


def sec_json(url):
    """Download one SEC JSON response using the required identifying User-Agent."""
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise ValueError(f"SEC EDGAR returned HTTP {error.code}.") from error
    except URLError as error:
        raise ValueError(f"Could not reach SEC EDGAR: {error.reason}") from error


def cik_for_ticker(ticker):
    """Look up and zero-pad the CIK for a ticker using the SEC ticker file."""
    wanted = ticker.strip().upper()
    for record in sec_json(TICKERS_URL).values():
        if record["ticker"].upper() == wanted:
            return str(record["cik_str"]).zfill(10)
    raise ValueError(f"Ticker {wanted} was not found in the SEC ticker file.")


def company_facts(ticker):
    """Return the SEC company-facts JSON for a ticker."""
    return sec_json(FACTS_URL.format(cik=cik_for_ticker(ticker)))


def annual_candidates(facts, tag, point_in_time):
    """Return USD 10-K candidates for a tag, filtered to annual flows or year-end points."""
    units = facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", [])
    candidates = []
    for fact in units:
        if fact.get("form") != "10-K" or not fact.get("end"):
            continue
        if point_in_time:
            if fact.get("start"):
                continue
        else:
            if not fact.get("start"):
                continue
            days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
            if not 300 <= days <= 380:
                continue
        candidates.append(fact)
    return candidates


def fiscal_year_ends(facts):
    """Find the last five annual 10-K fiscal year-end dates from the required facts."""
    ends = set()
    for tags in FLOW_METRICS.values():
        for tag in tags:
            ends.update(fact["end"] for fact in annual_candidates(facts, tag, point_in_time=False))
    return sorted(ends)[-5:]


def fact_for_year(facts, year_end, tags, point_in_time):
    """Return the first available required tag's latest-filed fact for one fiscal year."""
    for tag in tags:
        matches = [
            fact
            for fact in annual_candidates(facts, tag, point_in_time)
            if fact["end"] == year_end
        ]
        if matches:
            chosen = max(matches, key=lambda fact: fact.get("filed", ""))
            return {"value": chosen["val"] / 1_000_000, "tag": tag, "filed": chosen.get("filed", "")}
    return {"value": None, "tag": "not found", "filed": ""}


def format_value(value):
    """Format a dollar-million input or a missing value."""
    return "not found" if value is None else f"{value:,.0f}"


def format_percent(value):
    """Format a percent or an unknown calculation."""
    return "not known" if value is None else f"{value * 100:.1f}%"


def build_rows(facts):
    """Turn EDGAR facts into the last five fiscal-year rows and computed metrics."""
    rows = []
    for year_end in fiscal_year_ends(facts):
        row = {"Fiscal year end": year_end, "tags": {}}
        for label, tags in FLOW_METRICS.items():
            result = fact_for_year(facts, year_end, tags, point_in_time=False)
            row[label] = result["value"]
            row["tags"][label] = result["tag"]
        for label, tags in POINT_METRICS.items():
            result = fact_for_year(facts, year_end, tags, point_in_time=True)
            row[label] = result["value"]
            row["tags"][label] = result["tag"]
        row["ROE"] = (
            row["Net income"] / row["Equity"]
            if row["Net income"] is not None and row["Equity"] is not None and row["Equity"] > 0
            else None
        )
        row["Owner earnings"] = (
            row["Operating cash flow"] - row["Capital spending"]
            if row["Operating cash flow"] is not None and row["Capital spending"] is not None
            else None
        )
        rows.append(row)
    return rows


def buffett_checks(rows):
    """Compute the three checks, returning not known whenever a required input is missing."""
    roe = [row["ROE"] for row in rows]
    owner_earnings = [row["Owner earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": (
            "not known" if any(value is None for value in roe) else "pass" if all(value >= 0.15 for value in roe) else "fail"
        ),
        "Owner earnings positive every year": (
            "not known"
            if any(value is None for value in owner_earnings)
            else "pass" if all(value > 0 for value in owner_earnings) else "fail"
        ),
        "Owner earnings grew, first year to last": (
            "not known"
            if any(value is None for value in owner_earnings)
            else "pass" if owner_earnings[-1] > owner_earnings[0] else "fail"
        ),
    }


def analyze_ticker(ticker):
    """Download facts and return only code-computed data for a later memo judgment."""
    facts = company_facts(ticker)
    rows = build_rows(facts)
    if len(rows) < 5:
        raise ValueError("Fewer than five annual 10-K fiscal years were found.")
    return {"ticker": ticker.upper(), "company": facts.get("entityName", ticker.upper()), "rows": rows, "checks": buffett_checks(rows)}


def report_text(analysis):
    """Render the complete script output, including each source XBRL tag."""
    headings = ["Fiscal year end", "Revenue", "Net income", "Operating cash flow", "Capital spending", "Equity", "ROE", "Owner earnings"]
    lines = [f"{analysis['company']} ({analysis['ticker']}) — USD millions", " | ".join(headings)]
    for row in analysis["rows"]:
        lines.append(
            " | ".join(
                [
                    row["Fiscal year end"],
                    format_value(row["Revenue"]),
                    format_value(row["Net income"]),
                    format_value(row["Operating cash flow"]),
                    format_value(row["Capital spending"]),
                    format_value(row["Equity"]),
                    format_percent(row["ROE"]),
                    format_value(row["Owner earnings"]),
                ]
            )
        )
        lines.append("  XBRL tags: " + "; ".join(f"{label}={tag}" for label, tag in row["tags"].items()))
    lines.append("Buffett checks")
    lines.extend(f"{label}: {result}" for label, result in analysis["checks"].items())
    return "\n".join(lines)


def printed_number_tokens(analysis):
    """Return numeric tokens the deterministic report printed, for memo-audit use."""
    return set(re.findall(r"\b\d+(?:\.\d+)?%?", report_text(analysis)))


def main():
    """Run the EDGAR facts engine from the command line."""
    ticker = sys.argv[1] if len(sys.argv) > 1 else "COST"
    print(report_text(analyze_ticker(ticker)))


if __name__ == "__main__":
    main()
