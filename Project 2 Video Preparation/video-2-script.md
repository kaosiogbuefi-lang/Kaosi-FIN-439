# Video 2 Recording Guide - Code Walkthrough

**Target recording time:** about 4:30. Keep your webcam and microphone on throughout. Your webcam stays visible in the corner while VS Code, the app, and GitHub are shown.

## Before you press Record

1. Open the published `Project 2 Turn In` folder in VS Code.
2. Open these tabs in advance: `app.py`, `app_logic.py`, `portfolio.py`, `prices.csv`, `changed_input_reserve_test.py`, `docs/validation-and-ai-use.md`, and `output/changed-input-reserve-output.md`.
3. Have the live application open in a browser, plus the GitHub repository in another browser tab at `Project 2 Turn In/docs/validation-and-ai-use.md`.
4. Do not edit code or run either changed-input script while recording.

## Recording timeline and dialogue

| Time | Screen action | Spoken dialogue |
|---|---|---|
| 0:00-0:14 | **VS Code:** Show the published Project 2 Turn In folder and file list. | "Codex helped me implement and test this project, and an independent ChatGPT review checked calculations and suggested corrections. I am walking through the final code and results. This is educational, not investment advice." |
| 0:14-0:24 | **Switch to Application:** Show the default sidebar briefly. | "I will start with the app, then show where the calculations and controls live in code." |
| 0:24-0:50 | **Switch to VS Code, `app.py`:** Show the sidebar controls for objective, reserve, cost, replacement prices, and DGS10 evidence. | "`app.py` is the Streamlit interface. A committee can change the estimated return objective, the BIL-plus-IEF reserve minimum, an illustrative annual cost, replacement prices, and the DGS10 evidence status. The default 6.5% net-return target is a simplified model assumption, not a promise to achieve Meridian's CPI-plus-4% objective." |
| 0:50-1:22 | **VS Code, `app_logic.py`:** Find the price-validation function. Then click `prices.csv` to show the Date, BIL, IEF, LQD, and VT columns. | "Before optimization, the app validates the file. It expects exactly BIL, IEF, LQD, and VT; chronological monthly dates; no duplicates; no missing, non-finite, or non-positive prices; and at least 37 prices, which produces the 36 monthly returns needed for the stress window." |
| 1:22-1:52 | **VS Code, `portfolio.py`:** Find `estimate_from_csv`. | "`estimate_from_csv` turns adjusted-close prices into monthly returns. It annualizes the average monthly return by multiplying by 12, annualizes volatility using the square root of 12, and calculates correlations from the same return history. These are historical estimates, not forecasts." |
| 1:52-2:25 | **VS Code, `portfolio.py`:** Find the covariance and portfolio-volatility functions, then `search_lowest_risk_mix`. Scroll slowly. | "The covariance calculation combines each pair's correlation with both volatilities. Portfolio volatility then uses the portfolio weights and the covariance matrix, so diversification is included. `search_lowest_risk_mix` tries long-only five-point allocations, keeps only the mixes that meet the return target and reserve minimum, and picks the feasible one with the lowest volatility." |
| 2:25-2:55 | **VS Code, `app_logic.py`:** Show `evaluate`, `verdict`, and `build_project2_results`. | "`evaluate` calculates return, volatility, and reserve weight for every baseline or candidate. `verdict` reports which simplified rule passed or failed. `build_project2_results` creates equal weight, inverse volatility, Meridian's 60% VT and 40% LQD benchmark, the constrained base mix, and the last-36-return stress mix using the same engine." |
| 2:55-3:25 | **VS Code, `app_logic.py`:** Show recommendation logic and `constraint_safe_range`. | "The recommendation is centralized here instead of being hardcoded in the screen. If the base is infeasible, the process is rejected. If the stress mix is infeasible, it stops. A 25-point or larger allocation movement blocks full adoption. The range is shown only when the endpoints pass unrounded checks in both windows." |
| 3:25-3:50 | **Switch to Application:** Scroll to the DGS10 status, partial-month sensitivity, then the cost sensitivity table. | "The default DGS10 signal is a verified ALFRED vintage. A manual or unavailable rate is labeled unverified and stops implementation approval. The app keeps the partial October price row for reproducibility, but separately tests excluding it. It also tests illustrative costs of 0, 10, 25, and 50 basis points. At 50 basis points the base and stress BIL weights change to 55% and 80%, but the Pilot result remains." |
| 3:50-4:00 | **Switch to GitHub:** Open the published `validation-and-ai-use.md` page. Pause so the GitHub URL is visible. | "The validation record is also published in the repository so a reviewer can see the prediction and result." |
| 4:00-4:22 | **GitHub:** Scroll to the 2026-11-23 reserve-minimum changed-input section. | "For the completed locked changed-input test, I raised the reserve minimum from 3% to 90% before running the test. The prediction was committed and pushed first: both windows should become infeasible and the recommendation should be Reject." |
| 4:22-4:30 | **Switch to VS Code, `output/changed-input-reserve-output.md`:** Show the actual console output and comparison table. | "The actual result matched: both windows were infeasible, the centralized recommendation returned Reject, and no allocation range appeared. This is model-level support, not proof of full Meridian compliance." |

## Do not say or do

- Do not claim that a partner or human cold run was completed.
- Do not run the old `changed_input_test.py`; it is historical preliminary evidence.
- Do not present the simplified app verdict as full mandate compliance.

## Timing note

The last row should end at about **4:30**. If you lose time while clicking, shorten the explanation of annualization, not the recommendation or changed-input sections.
