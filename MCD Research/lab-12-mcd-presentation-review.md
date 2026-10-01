# Lab 12 — McDonald's Presentation and Partner Review

## Presentation route — McDonald's Corporation (NYSE: MCD)

**Valuation date / currency / share basis:** September 23, 2026 latest completed close; USD; 712.3M diluted weighted-average shares in the pro-forma. The share-price reference was $238.32. [Price source](https://www.financecharts.com/stocks/MCD/summary/price)

### 1. Target selection

I selected McDonald's because it is a global, public, predominantly franchised restaurant company with extensive primary filing evidence, positive earnings, observable market pricing, and a business model that can be traced from system sales to franchise fees, margins, cash flow, and equity value. My initial view was that it is a high-quality cash-generative business, but its value must be tested against its substantial debt and the price paid for the shares.

### 2. Company and evidence

McDonald's earns revenue from company-operated restaurant sales and from franchise fees, rent, and royalties. It was approximately 95% franchised at year-end 2025, which makes its high analytical gross margin structurally different from a company-operated restaurant or auto-dealer model. [2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm)

The financial-model history is FY2023–FY2025 in USD millions. FY2025 revenue was $26.885B, net income $8.563B, cash $774M, inventory $61M, net PP&E $28.241B, and debt carrying amount about $39.973B. The source table and calculations are in [Lab 10 assumptions](lab-10-mcd-assumptions.md).

### 3. Pro-forma

The model starts from the FY2025 balance sheet, projects FY2026–FY2030, calculates cash after linked operating, investing, and financing flows, and checks that assets less liabilities less equity equals zero in every usable run. The MCD-specific line is **no floor-plan financing**: inventory is small, is projected as a percentage of revenue, and is not funded by a dealer-style inventory-loan balance. The model uses a revenue-growth path of 4.0%, 4.0%, 3.5%, 3.0%, and 2.5%; 59.51% gross margin; 19.0% SG&A/gross profit; and capex beginning at the company-guided 2026 midpoint. [MCD pro-forma](lab%2010mcd_proforma.py)

### 4. Valuation

The pro-forma uses FCFE, an 8.0% cost of equity, 2.5% terminal growth, and 712.3M diluted shares. The base pro-forma value is **$168.25 per share**. Its limitation is that the terminal value, the simplified working-capital schedule, cost of equity, and fixed debt/buyback assumptions are judgments rather than market-proof facts.

The earlier DCF framework and peer P/E comparison answer different questions and should not be averaged. The peer P/E work produced a $309.82–$388.96 range from two qualified franchise-led peers, while the DCF base was $270.33 per share under its different FCFF and WACC assumptions. The peer range embeds the peers' capital structures and below-the-line earnings; the pro-forma is a separate FCFE model whose output is highly dependent on its cash-flow and terminal assumptions. See [Lab 08 peer comparison](lab-08-peer-comparison.md), [Lab 06 sources](lab-06-sources.md), and [reverse DCF model](Lab%206%20Reverse%20dcf.py).

### 5. Sensitivity and drivers

The Lab 11 revenue-growth sensitivity is the larger driver **over the ranges tested**. Lower/base/higher growth cases produced $156.49 / $168.25 / $180.44 per share, a $23.95 span. Gross-margin cases produced $163.57 / $168.25 / $172.84, a $9.26 span. The causal path is revenue growth → gross profit → operating income → net income and FCFE → value. This is not a forecast probability: the growth scenario has a wider total range than the gross-margin scenario. [Lab 11 results](lab-11-mcd-sensitivity.md) and [sensitivity runner](mcd_sensitivity.py).

### 6. Interpretation

**Conditional conclusion: watch-defer.** The company has strong franchise economics, but the valuation results disagree materially and the pro-forma base is below the observed market price. I would investigate the cost of equity, sustainable revenue growth, capital spending, and the treatment of cash, debt, and working capital before relying on a valuation conclusion. Evidence that sustained comparable sales, unit growth, margins, or cash conversion diverge from the forecast would change the view.

## Questions received as presenter and responses

| Question | Response / unresolved gap | Resulting action |
|---|---|---|
| Why does MCD have no floor-plan line? | Its filings describe a restaurant/franchise system rather than dealer inventory loans; inventory is $61M against $26.885B of revenue. | Keep “none” as the company-specific line; revisit only if filings identify comparable inventory financing. |
| Why does revenue growth rank above margin in sensitivity? | It does so only over the selected ranges; the growth range is wider and compounds through five years. | Keep the qualified ranking and do not call it a probability. |
| Why is the pro-forma value below the peer P/E range? | The FCFE model embeds specific cash-flow, terminal, debt, and buyback assumptions, while P/E carries peer capital structures and earnings conventions. | Investigate and reconcile the major convention differences rather than average them. |

## Review of partner — Microsoft

### Specific questions asked

1. **Selection and evidence:** Which Microsoft filing or earnings release supports the main growth claim, and is that claim about Azure, commercial cloud, software licensing, or another business line?
2. **Model and valuation:** How does the selected operating input flow through revenue, operating income, free cash flow, and value per share without double-counting a linked assumption?
3. **Sensitivity and interpretation:** Does the main driver rank first only because its lower/base/higher range is wider than the other range? What source or evidence would change the conclusion?

### Check and result

**Instructor-approved substitute check:** Microsoft's selected driver is organic revenue growth. The illustrative lower / base / higher growth paths are 8% / 10% / 12% in each forecast year. The base value per share is **$510.20** and the higher-growth value per share is **$539.50**. I recomputed the change as **$539.50 − $510.20 = +$29.30 per share**. Gross margin remained at 68.50%, capex remained at $65,000M per year, and unearned revenue remained at 22.91% of revenue; the accounting checks passed. These figures are an instructor-approved substitute for unavailable partner output.

### Explain-back and feedback

My understanding is that Microsoft's conclusion depends on the specific operating driver selected in its model—potentially cloud growth, Azure, commercial bookings, margins, or capital spending—because that driver affects revenue, operating income, free cash flow, and value. The main limitation is that a sensitivity ranking depends on the selected range and on whether the growth or margin evidence is already captured in the base forecast.

**Strength:** The selected Microsoft operating driver should provide an identifiable statement-level link rather than a generic terminal-value change.  
**Improvement:** Tie the lower/base/higher range to a primary Microsoft source and clearly distinguish Azure/cloud growth, pricing, margin, and capital-spending assumptions.

## Keep, revise, investigate

**Keep:** the franchise-led MCD model structure, the “no floor plan” treatment, and the qualified statement that revenue growth had the largest sensitivity span over the selected ranges.

**Revise:** do not rely on a single $168.25 pro-forma value as a decision answer; present it beside the disagreement with prior DCF and peer P/E work and name the convention differences.

**Investigate:** source a more complete WACC/cost-of-equity build, separate operating from excess cash, model receivables/payables/deferred revenue instead of the 0.8% working-capital placeholder, and test capex and share-repurchase policies.

The review does not change the watch-defer conclusion, but it changes the research priority: cash-flow-definition and discount-rate evidence comes before choosing between valuation outputs.

## Reflection and AI-use note

The question that most changed my emphasis was whether the growth ranking merely reflects its wider tested range. I now understand that sensitivity measures response over assumptions; it does not tell me how likely each case is. AI was not used during the live presentation/review; this file organizes the evidence and notes prepared beforehand.
