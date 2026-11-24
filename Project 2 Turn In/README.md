# Project 2 - Portfolio Decision System

**AI-assisted learning project; not investment advice.** Codex helped implement and test the app. An independent ChatGPT review reproduced the calculations and identified documentation and control corrections reflected here. The app reports model outputs; it does not establish that Meridian may implement a portfolio.

## Current model decision

**Pilot, not full adoption.** The default full-history model selects 60% BIL and 40% VT. The 36-month stress run selects 85% BIL and 15% VT, a 25.00-percentage-point movement that reaches the stability stop threshold.

The displayed executable pilot interval is a **joint** allocation rule, not four independent fund ranges:

- Lower endpoint: BIL 60.0000%, IEF 0.0000%, LQD 0.0000%, VT 40.0000%.
- Upper endpoint: BIL 64.9850%, IEF 0.0000%, LQD 0.0000%, VT 35.0150%.

Use one common blend between those endpoints. Both endpoints are retested with unrounded arithmetic under the full-history and last-36-return windows. Do not round the upper endpoint to 65.0% BIL; that would cross the active return boundary.

## Run

Tested environment: **Python 3.15.0** and **Streamlit 1.67.0**. `requirements.txt` specifies `streamlit>=1.40`.

```powershell
python --version
python -m pip install -r requirements.txt
streamlit run app.py
```

To regenerate the normal visible output only:

```powershell
python build_output.py
```

`changed_input_test.py` is the locked changed-input record. Do not rerun or modify it unless the course submission process specifically authorizes that step.

## What the model computes

- Validates a monthly `prices.csv` with exactly BIL, IEF, LQD, and VT, at least 37 prices / 36 returns, chronological consecutive months, no duplicates, and finite positive prices.
- Estimates annualized historical returns, volatility, and correlations from adjusted-close prices.
- Applies an editable illustrative annual cost overlay to estimated returns, then computes equal-weight, inverse-volatility, Meridian benchmark, and constrained portfolios.
- Compares full-history estimates with a last-36-month-return stress window.
- Shows an ALFRED-vintage DGS10 monitor. Manual DGS10 values remain unverified and stop implementation approval.

## Baselines and model constraints

The app displays three baselines: equal weight, inverse volatility, and Meridian's original 60% VT / 40% LQD benchmark. The simplified model applies a 6.5% estimated annual **net-return** target, a 3% BIL-plus-IEF reserve minimum, long-only weights, full investment, and a five-percentage-point search grid.

These are not full Meridian compliance. Meridian's original objective is CPI + 4% net of costs over rolling five-year periods. The app does not verify the seven-year horizon, annual rebalancing, quarterly $750,000 payouts, derivatives prohibition, five-day liquidity, 8% issuer limit, annual-turnover rule, or undefined 10% loss provision. A sub-25-point model result is therefore labelled **Model approval only**, never unconditional implementation approval.

## Data boundary and partial-month sensitivity

The default `prices.csv` is preserved for reproducibility: 60 monthly prices / 59 returns from 2021-11-01 through 2026-10-01. Its stated Yahoo Finance download date is 2026-10-22, before October 2026 ended, so the final October observation is partial.

The app retains that source row unchanged and separately excludes it in memory. Excluding it produces a 65% BIL / 35% VT base allocation with 6.54% estimated return, 5.32% volatility, and a 20-point movement. That is **Model approval only**, not implementation approval, because original Meridian conditions remain unresolved. The sensitivity matters because completed-month data can change an optimizer's allocation and apparent stability.

## Cost sensitivity

Costs are illustrative overlays, not verified fund-cost records; adjusted prices may already embed fund-level expenses.

| Annual cost | Base / stress allocation | Movement | Result |
|---|---|---:|---|
| 0 bp | 60/40 BIL/VT; 85/15 BIL/VT | 25 points | Pilot |
| 10 bp | 60/40 BIL/VT; 85/15 BIL/VT | 25 points | Pilot |
| 25 bp | 60/40 BIL/VT; 85/15 BIL/VT | 25 points | Pilot |
| 50 bp | 55/45 BIL/VT; 80/20 BIL/VT | 25 points | Pilot |

## Point-in-time DGS10 evidence

The default DGS10 evidence was independently checked against the [ALFRED 2026-10-29 vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-29): 2026-10-23 = 5.00%, 2026-10-26 = 5.00%, and 2026-10-27 = 4.99%. The app uses the 2026-10-27 observation as available by the 2026-10-29 vintage. This confirms the reported rows only; it does not create a retained downloaded source file or verify future manual values.

## Repository map

- `app.py` - Streamlit interface.
- `app_logic.py` - validation, recommendation, point-in-time status, and report logic.
- `portfolio.py` - reusable portfolio calculations and search.
- `prices.csv` - preserved source data.
- `build_output.py` and `output/visible-executed-output.md` - visible default-engine output.
- `docs/` - decision memo, validation/AI-use record, transcripts, and submission manifest.
