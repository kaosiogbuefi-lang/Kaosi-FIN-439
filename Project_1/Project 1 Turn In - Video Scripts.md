# Project 1 — Video Scripts

Use these as speaking notes, not as something you must read word-for-word. Keep the relevant file, terminal output, or workbench visible while you record. After recording, correct each transcript so its dates, values, and method names match the final project files.

## Video 1 — Research evolution

For this project, I evaluated McDonald's as a possible long-only investment. My valuation date is September 23, 2026, when the share price was $238.32. I used U.S. dollars in millions and 712.3 million diluted shares in the model.

The main thing I learned during the research was to separate facts from my own judgments. I used McDonald's FY2025 filing for historical revenue, inventory, property and equipment, cash, debt, and income-statement information. I then made clearly labelled forecast assumptions. Revenue growth declines from 4.0% to 2.5% over the forecast period. I held gross margin at a historical, franchise-focused level, and I used a stated capex forecast schedule.

The facts in the filing are the starting point, but the forecast is still based on assumptions. The information that could most change my conclusion would be future comparable sales, restaurant unit growth, margins, capex, interest expense, and debt disclosures.

I also used peer P/E and EV/EBITDA comparisons as cross-checks. I did not average those results with my DCF. Each method uses different assumptions and has different limitations. The P/E peer group is small, and QSR has a discontinued-operations issue. The EBITDA figures also need more reconciliation before I would place heavy weight on that method.

## Video 2 — Code and validation

This is my FCFF and WACC valuation model. The model projects McDonald's income statement, balance sheet, and cash flow from 2026 through 2030. It calculates free cash flow to the firm, or FCFF, by starting with NOPAT, adding depreciation, and subtracting capex, inventory investment, and other working-capital investment.

The model discounts those cash flows using a 7.05% WACC. It also calculates a terminal value at the end of 2030 and then moves from enterprise value to equity value by adding excess cash and subtracting debt.

I built checks into the code. The model checks the published synthetic DCF answer, the base-year balance sheet, the balance-sheet relationship in every forecast year, the cash-flow ties, and whether the DCF responds in the expected direction. In this output, all of those checks pass.

My base-case value is $183.15 per share. Terminal value makes up 81.3% of enterprise value, so I treat that as an important limitation because the result depends heavily on the assumptions after 2030.

For my downside sensitivity, I reduced every forecast revenue-growth rate by one percentage point. Before I ran it, I expected the value to decrease because lower revenue would reduce gross profit, EBIT, NOPAT, FCFF, and terminal value. The model produced $168.70 per share, compared with $183.15 in the base case. That result matched the direction I predicted.

## Video 3 — Live workbench demonstration and recommendation

I am starting with my McDonald's FCFF workbench. The base case is currently loaded. I will change the FY2026 revenue-growth assumption by a small, bounded amount and click Calculate. The workbench now shows the updated value per share and the change compared with the restored base case.

The reason this affects value is that revenue growth flows through revenue, gross profit, operating profit, cash flow, and eventually terminal value. I will now click Reset base so the original assumptions are back in place.

Next, I will demonstrate a failing check. When I click Demo failing check, the terminal-growth assumption becomes greater than or equal to WACC. That makes the terminal-value formula invalid, so the checks panel turns red instead of calculating a misleading value. I will reset the base case again to return the tool to a valid input set.

My recommendation is to watch McDonald's and defer starting a position at the September 23, 2026 reference price of $238.32. My FCFF DCF range is $168.70 to $198.15 per share, which is below the market price. In a reverse DCF, the market price requires a 3.51-percentage-point increase to every explicit five-year revenue-growth assumption while holding my other assumptions constant.

I am not saying the market is definitely wrong. I am saying that, under my model, the current price requires stronger growth than my base assumptions. I could change my decision if the stock price fell below a refreshed conservative FCFF range with an adequate margin of safety. I could also change my view if primary evidence supported sustainably higher growth or margins, lower capex needs, or a lower supportable WACC.

The main items I would monitor are comparable sales, unit growth, operating margin, capex guidance, interest expense, debt, and cash policy. The biggest limitation in my model is its dependence on terminal value, followed by my WACC and excess-cash assumptions. The peer P/E and EV/EBITDA results do not agree with the DCF, so I treat that disagreement as a question for more research rather than averaging the results.
