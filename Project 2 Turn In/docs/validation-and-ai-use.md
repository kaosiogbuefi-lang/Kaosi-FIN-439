# Project 2 — Validation and AI Use

**AI use:** Codex implemented and tested substantial parts of the application and documentation. An independent ChatGPT review reproduced calculations and proposed corrections. This is an AI-assisted learning demonstration, not investment advice.

## Purpose and decision boundary

This is an AI-assisted learning demonstration, not investment advice. The model searches long-only five-percentage-point allocations across BIL, IEF, LQD, and VT. It applies a simplified 6.5% estimated annual **net-return** target and a 3% BIL-plus-IEF reserve minimum. It is a screening model, not an execution system or proof of full Meridian mandate compliance.

## Data card and point-in-time boundary

| Field | Record |
|---|---|
| Price source | Yahoo Finance historical-data pages for BIL, IEF, LQD, and VT |
| Price field | Monthly Adjusted Close, oldest first |
| Stated download date | 2026-10-22 |
| Preserved source period | 2021-11-01 through 2026-10-01; 60 prices / 59 returns |
| October finding | The October 2026 monthly row was downloaded before 2026-10-31, so it is partial. The source file is retained unchanged for reproducibility. |
| Completed-month sensitivity | Excluding 2026-10-01 in memory leaves 58 returns and yields 65% BIL / 35% VT, 6.54% return, 5.32% volatility, and 20-point movement. |
| Rate signal | DGS10, daily 10-year Treasury constant-maturity yield, percent, not seasonally adjusted |
| Verified vintage source | [ALFRED DGS10 vintage 2026-10-29](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-29) |
| Verified observations | 2026-10-23 = 5.00%; 2026-10-26 = 5.00%; 2026-10-27 = 4.99% |
| Timing rule | Use only a verified ALFRED vintage available on the decision date. Manual entries are unverified; unavailable/unverified evidence stops implementation approval. |
| Evidence limitation | The application stores the reported values and source URL, not an archived downloaded ALFRED response; it cannot independently verify future manual observations. |

## Tests and results

| Test | Result | Meaning |
|---|---|---|
| Lab 14 known answer | Pass | Portfolio engine reproduced the course benchmark, equal-weight, and inverse-volatility values. |
| Lab 15 known answer | Pass | Search reproduced both Meridian runs. |
| Default constrained base | Pass | 60% BIL / 40% VT: 6.90% return, 6.01% volatility, 60.0% reserve eligibility. |
| Default window stress | Pilot | 85% BIL / 15% VT; largest movement is 25.00 points. |
| Meridian 60% VT / 40% LQD benchmark | Fails simplified reserve rule | 6.76% return, 12.30% volatility, 0.0% BIL-plus-IEF reserve. |
| Executable range endpoints | Pass | 60.0000% BIL / 40.0000% VT and 64.9850% BIL / 35.0150% VT pass unrounded checks in both windows. |
| Partial October exclusion | Model approval only | 65% BIL / 35% VT, 6.54% return, 5.32% volatility, 20-point movement; original mandate requirements remain unresolved. |
| Cost sensitivity | Pilot at 0, 10, 25, and 50 bp | All cases retain a 25-point movement; 50 bp changes the base/stress to 55/45 and 80/20 BIL/VT. |
| Replacement data length | Pass | Fewer than 37 prices / 36 returns is rejected before the stress test. |
| Manual DGS10 input | Stop | Manual input is labelled unverified and cannot support implementation approval. |
| ALFRED vintage query | Verified | Direct query returned the three stated DGS10 rows in the 2026-10-29 vintage response. |

## Limitations

- Historical returns, volatilities, and correlations are estimates, not forecasts.
- The October row is partial; preserving it is reproducible but completed-month sensitivity is material.
- The optimizer uses a coarse five-point search and can amplify small return-estimate changes.
- Cost cases are illustrative overlays, not verified fund-cost records, and could conceptually overlap with expenses reflected in adjusted prices.
- The DGS10 signal monitors rate conditions; it does not establish a return forecast. The external source response was queried but not archived in this repository.
- The simplified model does not verify several original Meridian conditions. It cannot grant implementation approval.

## Material AI use and checks

**Current disclosure (this table supersedes the historical draft entries below):**

| Tool / model | Interaction date | Material use | Check and disposition |
|---|---|---|---|
| Codex | 2026-11-18 to 2026-11-20 | Implemented validation, recommendation controls, executable endpoint logic, cost/partial-month sensitivities, and documentation edits | Ran engine tests, invalid-input tests, threshold checks, and normal visible-output generation. |
| ChatGPT, independent review | 2026-11-20 | Reproduced financial calculations, cost sensitivity, executable endpoints, partial-month sensitivity, and conditional recommendation logic; suggested corrections | Findings were incorporated into the app and documents. This was AI review, not human or partner verification. |
| Codex | 2026-11-20 | Queried the ALFRED vintage URL and compared DGS10 rows | Confirmed the three listed observations in the live vintage response; no downloaded response file was retained. |

### Superseded historical draft entries

| Tool / model | Interaction date | Material use | Check and disposition |
|---|---|---|---|
| Codex | 2026-11-18 | Helped integrate Lab 13–17 code into the app; drafted documentation and test scaffolding | Re-ran `python build_output.py`; compared base and stress values with the prior Lab 15 results; retained only computed output. |
| Codex | 2026-11-18 | Helped write the point-in-time data-card presentation | Checked source, units, release timing, and three DGS10 values against the saved Lab 17 data card. |

## Locked Changed-Input Record

**Record status:** prepared before the `changed_input_test.py` run. Commit this file before executing the run in the final repository; replace `COMMIT-PENDING` with the actual commit hash.

| Field | Record |
|---|---|
| Immutable commit / snapshot | `COMMIT-PENDING` |
| Input changed | Estimated annual return objective |
| Old value | 6.50% |
| New value | 7.50% |
| Prediction before run | Requiring the higher return will decrease BIL and increase VT in both windows, increasing volatility. The pilot recommendation will remain because the base and stress allocations will still differ materially. |
| AI condition | Drafted with Codex under the instructor-authorized full-AI workflow; retain this disclosure rather than presenting it as an AI-off prediction. |
| Command | `python changed_input_test.py` |
| Actual result | All months: 50% BIL / 50% VT, 7.69% return and 7.48% volatility. Last 36 returns: 80% BIL / 20% VT, 7.72% return and 2.33% volatility. Preserved in `output/changed-input-output.md`. |
| Decision effect | Pilot, not fully adopt, remains the decision. The base-to-stress gap is 30 points, above the 25-point stop condition. |
| Reconciliation / failure diagnosis | Prediction matched: raising the objective reduced BIL and increased VT in both windows, raising volatility. The larger window difference reinforced, rather than reversed, the pilot decision. |

## Cold-run record

The clean-user cold run must be completed from the repository README with no coaching. Record the command, first failure or “none,” elapsed time, and result location here after the partner test.
