# Lab 17 — Point-in-Time Audit

## App and known-answer checks

The point-in-time rate app is [`asof_app.py`](asof_app.py). It downloads current values from FRED and vintage values from ALFRED, without an API key.

| As known on | BAA | FEDFUNDS | DGS10 | MORTGAGE30US |
|---|---:|---:|---:|---:|
| 2026-10-05 | 6.47 | 3.75 | 5.28 | 7.28 |

PAYEMS probe: on 2025-01-15, December 2024 should read 159,536 as known then. The app's same-date revised count should be above zero because the current value has been revised.

## My series data card

- **Series ID:** DGS10
- **Source and link:** [FRED: DGS10](https://fred.stlouisfed.org/series/DGS10), sourced from the [Board of Governors of the Federal Reserve System's H.15 Selected Interest Rates release](https://www.federalreserve.gov/releases/h15/).
- **What it measures:** Market yield on U.S. Treasury securities at a constant maturity of ten years, quoted on an investment basis. It is relevant because changes in the benchmark Treasury rate affect the interest-rate sensitivity of the IEF Treasury-fund sleeve and the LQD investment-grade-bond sleeve.
- **Units:** Percent, not seasonally adjusted; daily frequency.
- **Publication lag:** About one business day. For example, the FRED page showed the 2026-10-27 observation on 2026-10-28 and listed the next release for 2026-10-29. The app's as-known-on date therefore excludes a value until the later publication date.
- **Revisions:** The series is a daily market rate, so the app should show little or no publication lag beyond the next business day and typically no same-date revisions. FRED nevertheless warns that all data are subject to revision; Project 2 must retain the ALFRED vintage check rather than assume revisions can never occur.
- **Download date:** 2026-10-29
- **Three values checked by hand against FRED:** 2026-10-27 = 4.99%; 2026-10-26 = 5.00%; 2026-10-23 = 5.00%.

## Partner attack and response

**Field challenged:** Revisions.

**Response:** DGS10 is a daily market rate, so the point-in-time app shows that the meaningful timing issue is whether the current business day's value had been published by the trade date, rather than a long monthly-release lag. The FRED page still states that all data are subject to revision, so I will use the ALFRED vintage as of each decision date and recheck the app's same-date revised count instead of relying on today's history.

## Project 2 call

**Decision:** Admit.

**Rule and condition:** Use only the DGS10 values available in ALFRED as of the portfolio decision date; do not use a current FRED value that appeared later. Reconsider this admission if the app shows material same-date revisions, if the source's publication timetable changes, or if the decision must be made before the daily H.15 value is published.
