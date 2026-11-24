# Video 3 Recording Guide - Investment Committee Presentation

**Target recording time:** about 4:30. Keep your webcam and microphone on throughout. Begin with the live application, as required. Keep the webcam box in a corner that does not cover the sidebar or metrics.

## Before you press Record

1. Run `streamlit run app.py` from the published `Project 2 Turn In` folder.
2. Keep the app at its defaults: 6.5% objective, 3.0% BIL + IEF reserve, 0 basis points cost, and **Verified ALFRED vintage (2026-10-29)**.
3. Open supporting tabs before recording: `docs/decision-memo.md` in VS Code and `output/changed-input-reserve-output.md` in VS Code. Keep GitHub open to the Project 2 folder, but use it only if you have extra time.
4. Do not change default inputs during the main presentation. The only screen movement should be scrolling and switching tabs.

## Recording timeline and dialogue

| Time | Screen action | Spoken dialogue |
|---|---|---|
| 0:00-0:14 | **Application:** Start at the top with the title and default sidebar visible. | "I used Codex for implementation and testing help, and an independent ChatGPT review to check calculations and suggest corrections. I am presenting this final model analysis and committee decision. This is an educational demonstration, not investment advice." |
| 0:14-0:38 | **Application:** Scroll to the Mandate section. Let the original objective and benchmark stay on screen. | "Meridian's original objective is CPI plus 4% net of costs over rolling five-year periods. Its original benchmark is 60% VT and 40% LQD. The mandate also includes a seven-year horizon, annual rebalancing, quarterly payouts, reserve, liquidity, issuer, turnover, and loss-provision requirements." |
| 0:38-0:55 | **Application:** Point to the current model target and hard constraint. | "This app does not claim to verify every one of those requirements. It models a simplified 6.5% estimated annual net-return target, a 3% BIL-plus-IEF reserve minimum, long-only fully invested portfolios, and annualized volatility. So this is model-level support, not implementation approval." |
| 0:55-1:27 | **Application:** Scroll through Equal Weight, Inverse Volatility, and the Meridian benchmark. Pause on each verdict. | "I show three transparent baselines. Equal weight estimates 3.28% return and inverse volatility estimates 3.47%; both fail the simplified return target. Meridian's 60% VT and 40% LQD benchmark estimates 6.76% return and 12.30% volatility, but it fails the reserve rule with zero percent in BIL or IEF." |
| 1:27-1:58 | **Application:** Scroll to the constrained all-months result. Keep weights and three metrics visible. | "With the full-history estimates, the lowest-risk feasible mix is 60% BIL and 40% VT. It has a 6.90% estimated net return, 6.01% volatility, and 60% reserve eligibility." |
| 1:58-2:21 | **Application:** Scroll to the recommendation range. Pause on the endpoint text. | "My recommendation is Pilot, not full adoption. For a model pilot, use one common blend between 60.0000% BIL and 40.0000% VT, and 64.9850% BIL and 35.0150% VT. IEF and LQD are zero at both endpoints. These are joint endpoints, not independent ranges. Do not round the upper BIL endpoint to 65%, because it would fail the active return boundary." |
| 2:21-2:48 | **Application:** Scroll to the last-36-return stress result and largest movement. | "The stress run uses only the last 36 monthly returns. It selects 85% BIL and 15% VT, with 6.87% estimated net return, 1.76% volatility, and 85% reserve eligibility. The 25-point movement from base to stress reaches my stability threshold, so full adoption is blocked." |
| 2:48-3:18 | **Application:** Scroll to the cost sensitivity table. Then scroll to the partial-final-observation sensitivity. | "For costs of 0, 10, and 25 basis points, the base stays 60/40 and stress stays 85/15. At 50 basis points they become 55/45 and 80/20, but the Pilot result remains. These costs are illustrative, not verified fund expenses. October 2026 was partial at download; excluding it in memory changes the base to 65% BIL and 35% VT, with 6.54% estimated return, 5.32% volatility, and 20-point movement." |
| 3:18-3:38 | **Application:** Scroll to DGS10 point-in-time evidence. | "The default rate monitor is DGS10 from the verified ALFRED vintage dated October 29, 2026. The October 27 observation is 4.99%. A manual or unavailable DGS10 value is unverified and stops implementation approval." |
| 3:38-3:43 | **Switch to VS Code:** Open `output/changed-input-reserve-output.md`. | "I will close with one validation check that is saved with the project." |
| 3:43-4:05 | **VS Code:** Show the input table and actual console output. | "In the completed locked changed-input test, I raised the reserve requirement from 3% to 90%. The prediction was committed before execution: both windows would be infeasible and the result would be Reject. The actual result matched. The app returned Reject instead of forcing an allocation." |
| 4:05-4:30 | **Switch back to Application:** Return to the recommendation and leave it on screen as you finish. | "My committee ask is approval to pilot the model output within the stated joint range, not approval to implement a portfolio. Return to committee review if either window is infeasible, movement reaches 25 points, DGS10 is unverified, a completed-month refresh changes the result, or any original mandate requirement remains unresolved. We still need evidence on liquidity, issuer exposure, payouts, turnover, derivatives, and the CIO's loss-provision interpretation." |

## Do not say

- Do not say that the model has full Meridian mandate compliance.
- Do not say that a human cold run was completed; it remains pending.
- Do not change the main app inputs live during this presentation. The sensitivity results are already visible in the app and report.
