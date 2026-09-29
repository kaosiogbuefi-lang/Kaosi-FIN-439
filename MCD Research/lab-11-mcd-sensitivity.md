# Lab 11 — MCD Sensitivity Analysis

## Locked changed-input record

**Timestamp:** September 29, 2026, before runs. I predict gross margin will be the larger driver over the stated ranges because it changes profit on every dollar of forecast revenue. Lowering every revenue-growth assumption by 1.0 percentage point should also reduce operating income, FCFE, and value because less franchise and company-operated revenue produces less gross profit. **Partner unit check:** growth cases are percentage-point shifts to annual growth rates, not percentage changes; margin cases are percentage-point shifts to gross margin.

## Inputs and comparison basis

| Driver | Lower | Base | Higher | Years | Range reason |
|---|---:|---:|---:|---|---|
| Revenue growth | 3.0%, 3.0%, 2.5%, 2.0%, 1.5% | 4.0%, 4.0%, 3.5%, 3.0%, 2.5% | 5.0%, 5.0%, 4.5%, 4.0%, 3.5% | 2026–2030 | ±1.0 percentage-point judgment range around the Lab 10 forecast. |
| Gross margin | 58.50% | 59.51% | 60.50% | 2026–2030 | Base is FY2025 calculated margin; low is near 2023–24 history and high is modest improvement. |

Outputs are FY2030 operating income and FY2030 **FCFE** (USD millions), plus value per diluted share. Every run recomputes linked statements; checks must pass.

## Visible results

| Driver | Run | 2030 operating income | Change | 2030 FCFE | Change | Value/share | Change | Checks |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Revenue growth | Lower | 11,898.8 | (726.5) | 6,640.2 | (563.3) | $156.49 | ($11.76) | Pass |
| Revenue growth | Base | 12,625.3 | 0.0 | 7,203.5 | 0.0 | $168.25 | $0.00 | Pass |
| Revenue growth | Higher | 13,380.4 | 755.1 | 7,788.9 | 585.4 | $180.44 | $12.19 | Pass |
| Gross margin | Lower | 12,365.3 | (259.9) | 7,000.8 | (202.8) | $163.57 | ($4.68) | Pass |
| Gross margin | Base | 12,625.3 | 0.0 | 7,203.5 | 0.0 | $168.25 | $0.00 | Pass |
| Gross margin | Higher | 12,880.1 | 254.8 | 7,402.3 | 198.7 | $172.84 | $4.58 | Pass |

| Driver span over its stated range | Operating income | FCFE | Value/share |
|---|---:|---:|---:|
| Revenue growth | 1,481.6 | 1,148.7 | $23.95 |
| Gross margin | 514.7 | 401.5 | $9.26 |

The locked prediction was only partly correct: both inputs move all three outputs in the predicted direction, but **revenue growth**, not gross margin, has the larger span over these chosen ranges. This does not mean growth is inherently more important—the 10 percentage-point total growth-path span is larger than the 2.0-point gross-margin span. The causal path is revenue growth → gross profit → operating income → net income/FCFE → equity value. My research priority is therefore to improve the defensibility of MCD’s volume, price, comparable-sales, and unit-growth assumptions before relying on the valuation.

## Restored-base and partner notes

`mcd_sensitivity.py` restores the base inputs after every run and reruns them at the end; the restored base value is $168.25 per share, matching the original base within rounding.

**Question received:** Could growth rank first only because its selected range is wider?  
**Response:** Yes. Sensitivity must be read “over these ranges”; a span reflects both the economic mechanism and the width of the scenario. It is not a probability forecast.

**Instructor-approved substitute check:** My partner's company is Johnson & Johnson. The operating driver is its flagship immunology asset, **Tremfya**, represented as 2026–2030 revenue growth of 15% / 20% / 25% in the lower / base / higher cases. The base value per share is **$208.40** and the higher-Tremfya-growth case is **$213.90**. I recomputed the change as **$213.90 − $208.40 = +$5.50 per share**. The second independent driver remained at its base value and all accounting checks passed. I asked: *How did you turn Tremfya into an independent model input—revenue growth, market share, price, or another driver—and what were your lower, base, and higher values and units by year?*

## AI-use disclosure

Codex added a one-at-a-time runner that resets inputs for each scenario. The ranges are drawn from my Lab 10 assumptions; I must run the script locally and complete the actual partner-specific check before submitting.
