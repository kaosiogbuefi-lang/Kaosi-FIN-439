# Project 1 Video Scripts and Screen Plan

Keep a small webcam view on in every video. Use the exact files below in the listed order. Speak naturally; these are notes, not something to read fast word-for-word. Correct the transcript after recording so it matches what you actually said.

## Video 1 - Research evolution and AI-output check

**Maximum length: 3 minutes.**

### Open these files in this exact order

1. `docs/edition-a-unchanged.md`
2. `docs/edition-b.md`
3. `docs/research-evolution.md`

### What to say

Hi, this is my Project 1 analysis of McDonald's. I am evaluating whether a long-only investment committee with no current MCD position should initiate a position.

This first file is my unchanged Edition A. My starting position was watch-defer. At that point, I thought McDonald's looked like a strong and cash-generative company, but I did not yet have a completed valuation, an updated share-count analysis, or a comparison with the market price. I identified those as the main things I still needed to research.

Now I am opening my Edition B. My final recommendation is still watch-defer, but it is more specific. My reference date is September 23, 2026, when MCD traded at $238.32. My FCFF model gives a range of $168.70 to $198.15 per share, which is below that price. So I would not initiate a position at the reference price.

The main change from Edition A to Edition B came from course instruction, my own analysis, and AI-assisted organizing, coding, and checking. I built a five-year FCFF model, added sensitivity and reverse-DCF analysis, and used peer P/E and EV-to-EBITDA as cross-checks.

This research-evolution file shows the change table. One AI-assisted suggestion was to use peer valuation beside my DCF. I checked that suggestion and qualified it instead of fully accepting it. P/E and FCFF use different valuation objects and capital-structure conventions. Also, the P/E group is small and QSR has a discontinued-operations issue. Because of that, I show the peer results separately and do not average them into my DCF.

The evidence that would change my view is stronger sustainable comparable sales, unit growth, margins, lower capital spending, or a lower supportable WACC. A lower market price could also create a sufficient margin of safety.

## Video 2 - Codebase walkthrough and validation

**Maximum length: 5 minutes.**

### Open these files in this exact order

1. `README.md`
2. `src/mcd_project1_fcff.py`
3. Terminal: run `py .\src\mcd_project1_fcff.py`
4. `visible-executed-output.txt`
5. `docs/validation-and-ai-use.md`

### What to say

This is the repository for my McDonald's valuation project. The README explains the decision, where the code is, the data sources, the run instructions, and the known limitations. The model uses only Python's standard library.

This file is the main FCFF engine. The model starts with financial statement inputs and forecasts McDonald's from 2026 through 2030. Revenue growth affects revenue, which affects profit and operating cash flow. The model calculates FCFF by taking operating profit after tax, adding depreciation, and subtracting capital spending, inventory investment, and other working-capital investment.

The model discounts the cash flows at a 7.05 percent WACC. It calculates terminal value at the end of 2030, then moves from enterprise value to equity value by adding excess cash and subtracting debt. Finally, it divides by diluted shares to calculate value per share.

I will now run the model from the terminal. The output includes the forecast, the valuation, and the validation checks. The base-case result is $183.15 per share.

The checks confirm the synthetic known answer, the base-year balance reconciliation, the forecast balance-sheet and cash-flow ties, and DCF monotonicity. In this output, the checks pass.

For my changed-input validation, I lowered every forecast-year revenue-growth rate by one percentage point while keeping the other independent assumptions fixed. Before I ran it, I predicted that lower revenue growth would lower operating profit, FCFF, terminal value, and value per share. The result dropped from $183.15 to $168.70 per share, so the result matched my prediction.

One important limitation is that terminal value is 81.3 percent of enterprise value. This means the valuation is sensitive to long-term growth and WACC assumptions, even though the model checks pass.

## Video 3 - Live product demonstration and committee recommendation

**Maximum length: 5 minutes. The live demo must be the opening.**

### Open these files/windows in this exact order

1. Terminal: run `py .\src\mcd_workbench.py`
2. Keep the FCFF Workbench visible for the entire video.
3. Optionally keep `docs/decision-memo.md` open behind the workbench for the final recommendation notes.

### What to do and say

This is my McDonald's FCFF workbench. I am starting with the documented base case loaded.

I am changing the FY2026 revenue-growth assumption by a small amount within the allowed range. Now I will click Calculate.

The value per share changed compared with the base case. This makes sense because revenue growth changes revenue first, then gross profit, operating profit, FCFF, and terminal value. I am now clicking Reset base to restore the documented assumptions.

Next, I will click Demo failing check. This makes terminal growth greater than or equal to WACC, which makes the terminal-value formula invalid. The workbench shows a clear failed check instead of producing a misleading number. I will now click Reset base again, so the model is back to a valid set of inputs.

My recommendation is watch-defer and do not initiate McDonald's at the $238.32 reference price. My FCFF range is $168.70 to $198.15 per share, which is below the market price. The base value is $183.15 per share.

The reverse DCF shows that, under my model, the market price requires adding 3.51 percentage points to every explicit annual revenue-growth assumption while keeping the other base assumptions fixed. That does not prove the market is wrong. It shows the amount of growth the market price requires under this model.

The main risks are weaker comparable sales, slower unit growth, lower margins, higher capex, higher interest expense, and higher debt. I would reconsider the decision if the price fell below a refreshed conservative value range with a sufficient margin of safety, or if primary evidence supported sustainably stronger growth or margins, lower capex, or a lower WACC.

My committee ask is to defer initiating a position and continue monitoring those operating and financing triggers.
