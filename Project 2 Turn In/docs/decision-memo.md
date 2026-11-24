# Project 2 Decision Memo

**AI-assisted learning demonstration; not investment advice.** Codex provided implementation/testing assistance, and an independent ChatGPT review reproduced calculations and suggested corrections. The application provides model-level results, not authority to implement a portfolio.

## Committee decision

**Pilot, not full adoption.** The all-months model selects 60% BIL / 40% VT with a 6.90% estimated net return, 6.01% volatility, and 60.0% reserve-eligible weight. The last-36-return stress model selects 85% BIL / 15% VT with a 6.87% estimated net return and 1.76% volatility. The 25.00-point allocation change reaches the model stability stop threshold.

If the committee authorizes only a model pilot, use one common blend between these executable, jointly constrained endpoints:

- 60.0000% BIL / 0.0000% IEF / 0.0000% LQD / 40.0000% VT
- 64.9850% BIL / 0.0000% IEF / 0.0000% LQD / 35.0150% VT

The endpoints are retested with unrounded arithmetic in both estimation windows. They are not independent sleeve ranges; do not round the upper BIL endpoint to 65.0%.

## Baselines and limits

Equal weight and inverse volatility miss the simplified 6.5% estimated net-return target. Meridian's original 60% VT / 40% LQD benchmark estimates 6.76% return and 12.30% volatility but fails the model's 3% BIL-plus-IEF reserve minimum at 0.0% reserve eligibility.

The model checks only a simplified historical return target, a reserve minimum, long-only/full-investment mechanics, and the five-point search. It does **not** establish compliance with Meridian's original CPI + 4% net-of-costs rolling-five-year objective, seven-year horizon, annual rebalancing, quarterly payouts, liquidity, issuer exposure, derivatives, turnover, or undefined loss provision. Therefore, even a sub-threshold result would be **Model approval only**, pending those original-mandate requirements.

## Data and sensitivity

The preserved default price file has 60 prices / 59 returns through 2026-10-01, but its stated download date is 2026-10-22. October was incomplete at download. The app keeps that row for reproducibility and separately excludes it in memory: the base changes to 65% BIL / 35% VT, 6.54% return, 5.32% volatility, and a 20-point movement. That result is Model approval only, not implementation approval.

Illustrative annual costs of 0, 10, and 25 bp retain 60/40 base and 85/15 stress allocations; 50 bp produces 55/45 base and 80/20 stress. Every case retains a 25-point movement and Pilot result. These are sensitivity overlays, not verified fund costs; adjusted prices may already reflect expenses.

The DGS10 default was independently checked against the [ALFRED 2026-10-29 vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-29): 2026-10-23 = 5.00%, 2026-10-26 = 5.00%, 2026-10-27 = 4.99%. Unverified or unavailable DGS10 input stops implementation approval.

## Required monitoring

Pause or return to committee review if any base/stress allocation becomes infeasible, the stability threshold is reached, the DGS10 vintage is unverified or unavailable, a completed-month refresh changes the result, or any original-mandate requirement remains unresolved.
