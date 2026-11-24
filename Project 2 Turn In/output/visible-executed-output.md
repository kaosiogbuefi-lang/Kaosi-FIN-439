# Project 2 visible executed output

As-of price download: 2026-10-22. DGS10 data-card download: 2026-10-29.
Objective: 6.50% estimated annual net return. Reserve minimum: 3.0% in BIL + IEF.
Illustrative annual cost overlay: 0 basis points. Gross historical estimates are reduced by this overlay; it is not a verified fund-cost record.
Validated price coverage: 2021-11-01 through 2026-10-01 (60 observations; 59 monthly returns).
DGS10 vintage status: verified. Verified directly against the ALFRED vintage: DGS10 4.99% for 2026-10-27, available by 2026-10-29. Source: https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-29

Partial-final-observation warning: the final monthly row is partial because its recorded download date preceded that month-end. prices.csv is retained unchanged; see the in-memory exclusion sensitivity below.

## Equal weight
Weights: BIL 25.0% / IEF 25.0% / LQD 25.0% / VT 25.0%
Expected return: 3.28%
Volatility: 7.55%
Reserve-eligible: 50.0%
Mandate verdict: FAIL — failed: return objective

## Inverse volatility
Weights: BIL 87.7% / IEF 5.3% / LQD 4.2% / VT 2.8%
Expected return: 3.47%
Volatility: 1.32%
Reserve-eligible: 93.1%
Mandate verdict: FAIL — failed: return objective

## Meridian benchmark — 60% VT / 40% LQD
Weights: BIL 0.0% / IEF 0.0% / LQD 40.0% / VT 60.0%
Expected return: 6.76%
Volatility: 12.30%
Reserve-eligible: 0.0%
Mandate verdict: FAIL — failed: reserve minimum

## Constrained, all months
Weights: BIL 60.0% / IEF 0.0% / LQD 0.0% / VT 40.0%
Expected return: 6.90%
Volatility: 6.01%
Reserve-eligible: 60.0%
Mandate verdict: PASS

## Constrained, last 36 monthly returns
Weights: BIL 85.0% / IEF 0.0% / LQD 0.0% / VT 15.0%
Expected return: 6.87%
Volatility: 1.76%
Reserve-eligible: 85.0%
Mandate verdict: PASS

Largest base-to-stress allocation change: 25.00 percentage points.
Stop condition: 25 percentage points or more, or no feasible stress allocation.
The 25-point stability threshold is a model-sensitivity control, not the original 25% annual-turnover restriction.
Original Meridian mandate: the 6.5% target is a simplified modeling assumption; it does not verify CPI + 4% net of costs over rolling five-year periods.
Recommendation: Pilot
Do not fully adopt: the calculated base-to-stress allocation change is 25.00 percentage points, at or above the 25-point stability threshold.
Constraint-safe allocation range endpoints:
Lower executable endpoint (stress blend 0.00%): BIL 60.0000% / IEF 0.0000% / LQD 0.0000% / VT 40.0000%
Upper executable endpoint (stress blend 19.94%): BIL 64.9850% / IEF 0.0000% / LQD 0.0000% / VT 35.0150%
Endpoint verification (all months / last 36): lower [True, True]; upper [True, True].
The displayed endpoints are conservative executable allocations at 0.0001 percentage-point precision. Each is retested with unrounded arithmetic under both estimation windows; do not round them to fewer decimals.

## Illustrative annual-cost sensitivity
0 bp: base BIL 60.0% / IEF 0.0% / LQD 0.0% / VT 40.0%; stress BIL 85.0% / IEF 0.0% / LQD 0.0% / VT 15.0%; movement 25.00 points; recommendation Pilot.
10 bp: base BIL 60.0% / IEF 0.0% / LQD 0.0% / VT 40.0%; stress BIL 85.0% / IEF 0.0% / LQD 0.0% / VT 15.0%; movement 25.00 points; recommendation Pilot.
25 bp: base BIL 60.0% / IEF 0.0% / LQD 0.0% / VT 40.0%; stress BIL 85.0% / IEF 0.0% / LQD 0.0% / VT 15.0%; movement 25.00 points; recommendation Pilot.
50 bp: base BIL 55.0% / IEF 0.0% / LQD 0.0% / VT 45.0%; stress BIL 80.0% / IEF 0.0% / LQD 0.0% / VT 20.0%; movement 25.00 points; recommendation Pilot.
Costs are illustrative overlays, not verified fund-cost records; adjusted prices may already reflect fund expenses.

## Partial-final-observation sensitivity
Excluded 2026-10-01 in memory only; prices.csv is unchanged. Remaining coverage: 2021-11-01 through 2026-09-01 (58 returns).
## Partial sensitivity, all remaining months
Weights: BIL 65.0% / IEF 0.0% / LQD 0.0% / VT 35.0%
Expected return: 6.54%
Volatility: 5.32%
Reserve-eligible: 65.0%
Mandate verdict: PASS

## Partial sensitivity, last 36 remaining returns
Weights: BIL 85.0% / IEF 0.0% / LQD 0.0% / VT 15.0%
Expected return: 6.75%
Volatility: 1.79%
Reserve-eligible: 85.0%
Mandate verdict: PASS

Partial sensitivity movement: 20.00 percentage points.
Partial sensitivity recommendation: Model approval only. The calculated stress movement is 20.00 percentage points, below the 25-point stability threshold, but implementation approval is not allowed until these original-mandate requirements are verified or resolved: Original return objective, Seven-year horizon and annual rebalancing, Quarterly $750,000 payouts, No derivatives, 90% redeemable within five business days, 8% maximum single-company exposure, 25% annual turnover without committee approval, 10% calendar-year loss provision.
