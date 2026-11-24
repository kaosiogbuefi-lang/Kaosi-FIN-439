# Video 1 Recording Guide - System Change, Thinking Change, and AI Check

**Target recording time:** about 2:40. Keep your webcam and microphone on throughout. Leave your webcam box in one corner; do not cover the app's main results or sidebar.

## Before you press Record

1. In the published `Project 2 Turn In` folder, run `streamlit run app.py`.
2. In the browser, leave these default inputs visible: 6.5% objective, 3.0% BIL + IEF reserve, 0 basis points cost, and **Verified ALFRED vintage (2026-10-29)**.
3. Open these backup tabs: the live application, `output/visible-executed-output.md` in VS Code, and `docs/decision-memo.md` in VS Code.
4. Start on the live application. Speak a little slower than normal so the recording stays under three minutes even with clicks.

## Recording timeline and dialogue

| Time | Screen action | Spoken dialogue |
|---|---|---|
| 0:00-0:12 | **Application:** Stay at the top of the app. Pause briefly so the title and sidebar are readable. | "I used Codex to help implement and test this project, and an independent ChatGPT review checked calculations and suggested corrections. I am presenting the final model results and decision. This is for education, not investment advice." |
| 0:12-0:27 | **Application:** Point to the default sidebar inputs, then scroll to the Mandate heading. | "My earlier tool just found a low-risk mix that met a return target and reserve rule. Project 2 changed it into a committee-facing app with controls, baselines, a stress run, a data-timing check, and a decision rule." |
| 0:27-0:48 | **Application:** Scroll through Equal Weight, Inverse Volatility, and Meridian benchmark. Pause on the benchmark verdict. | "The app now shows three transparent baselines: equal weight, inverse volatility, and Meridian's original 60% VT and 40% LQD benchmark. The benchmark estimates a 6.76% return and 12.30% volatility, but it fails the simplified reserve rule because it has zero percent in BIL or IEF." |
| 0:48-1:12 | **Application:** Scroll to the constrained all-months result. Put the 60% BIL / 40% VT weights and metrics on screen. | "The important change in my thinking is that meeting a return target does not automatically mean the answer is ready to use. The default base mix is 60% BIL and 40% VT. It estimates a 6.90% net return, 6.01% volatility, and 60% reserve eligibility." |
| 1:12-1:31 | **Application:** Scroll to the last-36-return stress result and then the recommendation. | "When I use only the last 36 monthly returns, the mix changes to 85% BIL and 15% VT. That is a 25-point movement. Because that reaches my stability threshold, the app says Pilot, not full adoption." |
| 1:31-1:36 | **Switch to VS Code:** Open `output/visible-executed-output.md`; keep webcam visible. | "Next, I will show one AI-assisted output that I checked against the visible engine report." |
| 1:36-2:04 | **VS Code:** Show the recommendation range lines. Highlight or point to both endpoints and the unrounded-check note. | "The lower endpoint is 60.0000% BIL and 40.0000% VT. The upper endpoint is 64.9850% BIL and 35.0150% VT. I checked that these are joint endpoints, not four separate fund ranges, and that both endpoints were retested with unrounded calculations in both windows. I do not round the upper BIL endpoint to 65%, because that would cross the active return boundary." |
| 2:04-2:24 | **VS Code:** Scroll to Partial-final-observation sensitivity. | "I also checked the completed-month sensitivity. October 2026 was a partial observation because the source was downloaded before month-end. Excluding it in memory changes the base result to 65% BIL and 35% VT, with 6.54% estimated return and 5.32% volatility. That is why I treat these as estimates, not forecasts." |
| 2:24-2:40 | **Switch back to Application:** Show recommendation and DGS10 status. | "My decision is to pilot the model only. I would return to committee review if either window becomes infeasible, movement reaches 25 points or more, DGS10 is unverified, a completed-month refresh changes the result, or original Meridian requirements remain unresolved." |

## Do not say

- Do not say that a human cold run was completed; it is still pending.
- Do not say the app proves full Meridian mandate compliance.
- Do not change any inputs during this video; use the default display only.
