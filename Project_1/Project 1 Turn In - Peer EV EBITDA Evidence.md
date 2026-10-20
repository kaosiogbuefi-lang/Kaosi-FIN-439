# MCD EV/EBITDA Comparable Analysis

**As-of date:** September 11, 2026. **Convention:** trailing enterprise value / trailing EBITDA; USD millions except per-share outputs.

## Policy and definitions

The same franchise-led restaurant policy used for the P/E work is applied: YUM and QSR are accepted/qualified global franchise-system peers, while DPZ is a qualified peer because its single-category pizza/delivery exposure is narrower than MCD’s system. EV/EBITDA is an enterprise multiple: it is applied to MCD EBITDA to estimate enterprise value, then cash is added and debt is deducted before dividing by diluted shares. This differs from P/E, which is already an equity multiple and must not be bridged again.

## Inputs and source reconciliation

| Company | TTM EV/EBITDA | Date / source | Qualification |
|---|---:|---|---|
| MCD | 15.57x; EV $232.483B | September 11, 2026, [MCD ratios](https://stockanalysis.com/stocks/mcd/financials/ratios/) | Target; provider EV and trailing ratio imply $14.931B trailing EBITDA. |
| YUM | 16.68x | September 11–13, 2026, [YUM statistics](https://stockanalysis.com/stocks/yum/statistics/) | Accepted; franchise-led but different brand/geographic mix. |
| QSR | 16.94x | September 11–13, 2026, [QSR statistics](https://stockanalysis.com/stocks/qsr/statistics/) | Qualified; higher leverage and different brand mix. |
| DPZ | 14.92x | September 11–13, 2026, [DPZ statistics](https://stockanalysis.com/stocks/dpz/statistics/) | Qualified; pizza/delivery concentration. |

For the enterprise-to-equity bridge, cash of $822M, debt fair value of $38.3B, and diluted weighted-average shares of 712.3M are from MCD’s June 2026 10-Q. [10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm)

## Output

The minimum/median/maximum peer multiples are 14.92x / 16.68x / 16.94x. Applying them to inferred MCD EBITDA produces approximately **$260.14 / $297.04 / $302.49 per share**. Run `python ".\\MCD Research\\mcd_ev_comparables.py"` from the repository root to reproduce the table.

## Limitation

These provider-supplied trailing ratios must be reconciled to each issuer’s underlying EBITDA definition before a final committee recommendation relies on them. The result is therefore a market cross-check, not a mechanically averaged value with the FCFF DCF or P/E method.
