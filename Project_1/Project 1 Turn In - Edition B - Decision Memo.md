# Project 1 — Edition B: McDonald's Corporation (MCD)

## Committee decision

**Action: Watch-defer; do not initiate at the September 23, 2026 reference price of $238.32.** The base FCFF DCF indicates $183.15 per diluted share, with a low/base/high range of $168.70–$198.15. The market price is above the high case. This is a watch-defer rather than a permanent rejection because the result remains sensitive to WACC, terminal growth, cash/debt treatment, and operating-growth assumptions.

**User / horizon / security / date / units:** Long-only public-equity fund with no position; seven-year analytical horizon and a five-year forecast; MCD common stock; September 23, 2026 reference close; USD millions except per-share values; 712.3M diluted weighted-average shares. Older FCFE pro-forma work is retained as supporting analysis; this Edition B decision uses the FCFF/WACC enterprise-value framework.

## Valuation evidence

| Item | Result | Basis |
|---|---:|---|
| FCFF DCF base value | $183.15/share | Five-year MCD pro-forma and FCFF DCF. |
| Low / base / high cases | $168.70 / $183.15 / $198.15 | Uniform -1.0 / 0.0 / +1.0 percentage-point shifts to each annual revenue-growth assumption. |
| WACC | 7.05% | 8.0% cost of equity; 3.87% pre-tax debt cost; market-equity and debt weights; 22.0% tax assumption. |
| Terminal growth | 2.5% | Long-run judgment, below WACC. |
| Enterprise value | $170,158.6M | PV explicit FCFF plus terminal value. |
| Enterprise-to-equity bridge | EV + $274.0M excess cash − $39,973.0M debt = $130,459.6M equity | Excess cash is reported cash less the $500M operating-cash floor. |
| Terminal value share | 81.3% of EV | Material limitation: most value is beyond the explicit forecast. |
| Reverse DCF | +3.51 percentage points to each explicit annual growth rate | Holds WACC, terminal growth, current debt/excess cash, and shares fixed to match $238.32. |

The base forecast revenue-growth path is 4.0%, 4.0%, 3.5%, 3.0%, and 2.5%. The reverse-DCF result therefore requires an approximately 7.51%, 7.51%, 7.01%, 6.51%, and 6.01% path instead. That is the market expectation under this model, not proof that the market is wrong.

## Sensitivity and downside

| WACC / terminal growth | 2.0% | 2.5% | 3.0% |
|---|---:|---:|---:|
| 6.55% | $187.41 | $212.90 | $245.58 |
| 7.05% | $163.08 | $183.15 | $208.18 |
| 7.55% | $143.15 | $159.30 | $178.99 |

**Named downside:** reduce every explicit revenue-growth input by one percentage point. Value falls to $168.70 per share because lower revenue lowers gross profit, EBIT, NOPAT, FCFF, and terminal value. This downside supports the current watch-defer action.

## Material evidence, normalizations, and challenges

| Load-bearing item | Value / basis | Challenge | Evidence that would change it |
|---|---|---|---|
| Revenue growth | 4.0%, 4.0%, 3.5%, 3.0%, 2.5%; judgment anchored to recent history | Mature-system growth may be lower, while unit development or pricing may be stronger. | Subsequent comparable sales, system-sales, unit-growth, and revenue releases. |
| Gross margin | 59.51%; calculated FY2025 franchise-led margin | The analytical subtotal is not a conventional reported gross-profit line. | Filing evidence of durable franchise/company-operated mix or margin change. |
| Capex | $3.8B, $4.2B, $4.0B, $3.9B, $3.9B | Later years are judgment rather than management guidance. | New capex guidance or restaurant-development plan. |
| WACC | 7.05%; model input build | Cost of equity and debt weights require continued market-input review. | Updated beta, risk-free rate, ERP, debt yields, and market capitalization. |
| Excess cash | $274M; $774M reported cash less $500M operating floor | Required operating cash has not been separately proven. | Liquidity policy, working-capital needs, and debt-note evidence. |
| Debt | $39.973B | Debt is material to per-share value; carrying versus fair-value choice changes the bridge. | Latest debt-note/fair-value disclosure. |

Historical MCD evidence and primary filing links are in the source map and supporting analysis. The three-statement model and full terminal output are included in this submission folder.

## Usable product: semi-adjustable FCFF workbench

The locally runnable [FCFF workbench](MCD%20Research/mcd_workbench.py) exposes only bounded, load-bearing assumptions: each forecast-year revenue growth rate (0%--6%), gross margin (58%--61%), WACC (6%--8%), and terminal growth (2%--9%, with terminal growth required to remain below WACC). The accounting engine, source/provenance record, enterprise-to-equity bridge, and articulation checks remain locked. It shows the live five-year results, valuation, terminal-value share, one-at-a-time growth cases, and WACC--growth sensitivity; **Reset base** restores the documented case and **Demo failing check** deliberately makes terminal growth exceed WACC so the checks panel turns red.

## Method disagreement

The peer P/E comparison of two qualified franchise-led peers implied $309.82–$388.96 per share, while the FCFF DCF base implies $183.15. These methods should not be averaged. P/E embeds peers’ capital structures, below-the-line earnings, and the selected peers’ market pricing; FCFF values MCD operating cash flows and then explicitly bridges debt and excess cash. The P/E work is useful as a challenge, but its two-peer sample and QSR’s discontinued-operation effect are material limitations. See the included Peer P/E Evidence file.

## Validation record

| Validation | Result |
|---|---|
| Synthetic known-answer reconciliation | $27.4974 per share, pass. |
| Base-year balance reconciliation | $0.0 gap, pass. |
| Five-year balance-sheet articulation | $0.0 / -$0.0 / $0.0 / $0.0 / $0.0 gaps, pass. |
| Cash-flow ties to cash | $0.0 gap in every forecast year, pass. |
| DCF monotonicity | Higher WACC lowers value; higher terminal growth raises value, pass. |
| Enterprise-to-equity bridge | EV, excess cash, debt, and diluted shares shown explicitly, pass. |
| Changed-input prediction and actual result | A pre-run sensitivity record predicted lower growth reduces operating income, FCFE, and value; direction held. The FCFF downside case also falls to $168.70. |
| AI output disposition | Accepted with qualification: AI identified QSR discontinued-operation effects; the 10-K confirmed the issue and it remains disclosed in the peer comparison. |

## Conditional reversal and monitoring triggers

Initiate only if one of two things occurs: (1) the market price falls below a refreshed conservative FCFF range with a defined margin of safety, or (2) primary evidence supports a sustained growth, margin, capex, or WACC revision sufficient to lift the FCFF value above price. Do not initiate if next results show weaker comparable sales, lower franchise/company-operated margins, higher reinvestment needs, or a higher supportable WACC.

Monitor global and U.S. comparable sales, system-unit growth, operating margin, capex guidance, interest expense/debt, and any change to the company’s liquidity or share-repurchase policy.
