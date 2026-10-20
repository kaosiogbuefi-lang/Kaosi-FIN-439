# Validation and AI-Use Record - Project 1: McDonald's (MCD)

## Validation evidence

| Check | Result | Evidence |
|---|---|---|
| Synthetic DCF known answer | Pass: $27.4974 per share | `../visible-executed-output.txt` |
| Base-year balance reconciliation | Pass: 0.0 gap | `../visible-executed-output.txt` |
| Annual balance-sheet and cash-flow ties | Pass in FY2026E-FY2030E | `../visible-executed-output.txt` |
| DCF monotonicity | Pass: higher WACC lowers value; higher terminal growth raises value | `../visible-executed-output.txt` |
| FCFF downside sensitivity | Pass: -1.0 percentage point growth shift lowers value from $183.15 to $168.70 | `../visible-executed-output.txt` |

## Locked changed-input record

**Material input:** Uniform FY2026-FY2030 revenue-growth-rate shift in the FCFF model.

**Base values:** 4.0%, 4.0%, 3.5%, 3.0%, and 2.5%.

**Changed values:** Each annual rate reduced by 1.0 percentage point, with WACC, terminal growth, debt, cash, capex, tax rate, and diluted shares held at base values.

**Prediction made before the run:** Lower growth should reduce revenue, gross profit, EBIT, NOPAT, FCFF, terminal value, and value per share. The recommendation should remain watch-defer if the output remains below the market price.

**Actual result:** Value per share declined from $183.15 to $168.70. The direction matched the prediction, and the recommendation remained watch-defer.

**Required student completion before freezing:** Enter the actual pre-run timestamp, Git commit hash, and preserved before/after output reference below. Do not invent these details.

| Required field | Student entry |
|---|---|
| Prediction timestamp | [ENTER ACTUAL TIMESTAMP] |
| Commit hash before changed-input run | [ENTER ACTUAL COMMIT HASH] |
| Before/after output file or screenshot | [ENTER PATH OR LINK] |

## Material AI-use disclosure

AI assistance was used for tasks requested in the course workflow: organizing project files, drafting and debugging Python code, explaining financial-model concepts, helping format written materials, locating potential source sections, and checking arithmetic and model logic. The submitted financial claims were checked against the cited filings or model output, and the student is responsible for the final recommendation and presentation.

## AI-output check

AI suggested presenting peer valuation methods alongside the FCFF DCF. I accepted that only with qualification after checking the comparability evidence. The final analysis does not average the methods because P/E, EV/EBITDA, and FCFF use different valuation objects and conventions. QSR's discontinued-operations issue and unreconciled provider EBITDA definitions remain disclosed limitations.
