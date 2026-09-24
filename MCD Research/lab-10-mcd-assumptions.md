# Lab 10 — McDonald's Through the Pro-Forma Engine

## Company-specific line

McDonald's is a primarily franchised restaurant system, not an auto dealer: it has **no floor-plan inventory financing**. Inventory is very small relative to revenue, so the model uses an inventory-to-revenue ratio and does not add a floor-plan debt line. This changes the cash-flow bridge: no increase in floor-plan borrowing offsets inventory investment.

## Three-year history and sources

All amounts are USD millions. Gross profit is a calculated analytical subtotal: franchised restaurant margin + company-operated restaurant margin + other revenue. McDonald's does not report a conventional single gross-profit line.

| Item | 2023 | 2024 | 2025 | Filing source |
|---|---:|---:|---:|---|
| Revenue | 25,494 | 25,920 | 26,885 | [2023 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390824000072/mcd-20231231.htm), [2024 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390825000012/mcd-20241231.htm), [2025 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm), Consolidated Statements of Income / MD&A operating results. |
| Gross profit (calculated) | 14,795 | 15,048 | 15,999 | Same filings; derived from reported franchised margins, company-operated margins, and other revenue. |
| SG&A | 2,817 | 2,858 | 3,039 | Same filings, MD&A operating results. |
| Net income | 8,469 | 8,223 | 8,563 | Same filings, Consolidated Statements of Income. |
| Inventory | 53 | 56 | 61 | 2024 10-K balance sheet reports 2024/2023; 2025 10-K balance sheet reports 2025/2024. |
| Net PP&E | 24,908 | 25,295 | 28,241 | 2024 10-K Property and Equipment note reports 2024/2023; 2025 10-K note reports 2025/2024. |
| Shareholders' equity (deficit) | (4,707) | (3,797) | (1,791) | 2024 and 2025 10-K balance sheets. |

**Hand checks:** 2025 revenue is $26,885M and 2025 inventory is $61M in the 2025 10-K balance sheet/MD&A. These checks confirm the latest historical base used in the model.

## History ratios

| Ratio or metric | 2023 | 2024 | 2025 | Interpretation |
|---|---:|---:|---:|---|
| Reported revenue growth | 10.0% | 1.7% | 3.7% | Revenue growth slowed after the 2023 rebound. |
| Gross margin (calculated) | 58.0% | 58.1% | 59.5% | Franchise-led revenue creates a high analytical gross margin. |
| SG&A / gross profit | 19.0% | 19.0% | 19.0% | Stable support-cost ratio. |
| Inventory / revenue | 0.21% | 0.22% | 0.23% | Small inventory base; no floor-plan line. |
| D&A / opening net PP&E | unresolved | 6.0% | 7.8% | 2025 uses $2,199M cash-flow-statement D&A divided by $28,241M year-end PP&E as a transparent simplification; the measure mixes leased and owned assets. |
| Capital expenditure | 2,761 | 2,775 | 3,365 | From cash-flow statements; 2025 10-K says 2026 capex guidance is $3.7B–$3.9B. |
| Effective tax rate | 20.3% | 20.7% | 21.7% | Derived from reported tax provision / pretax income. |
| Global comparable sales | 9.0% | 1.9% | 3.1% | Same-store / organic-style metric; it excludes FX and reflects restaurants open at least 13 months. |

## Assumption set

| Assumption | Value | Label | Reason |
|---|---:|---|---|
| Revenue growth, 2026–2030 | 4.0%, 4.0%, 3.5%, 3.0%, 2.5% | judgment | Begins around 2025's 3.7% reported growth and 3.1% global comparable-sales growth, then fades for a mature global system. |
| Gross margin | 59.51% | history | FY2025 calculated margin; retained because the franchise mix is structural. |
| SG&A / gross profit | 19.0% | history | Consistent with the three-year calculated ratio. |
| Depreciation / opening PP&E | 7.79% | history / simplification | FY2025 reported D&A divided by FY2025 net PP&E; refine when owned and leased assets are separated. |
| Impairment | 0 | judgment | No recurring annual impairment is forecast; a recurrence would lower earnings and cash flow. |
| Capex | 3,800; 4,200; 4,000; 3,900; 3,900 | guidance / judgment | 2026 midpoint of company guidance; 2027 incorporates management's indicated sequential increase; later years normalize. |
| Tax rate | 22.0% | history / judgment | Near the FY2025 21.7% effective rate. |
| Inventory / revenue | 0.227% | history | FY2025 inventory divided by revenue. |
| Floor-plan financing | none | fact / company-specific line | No comparable dealer inventory-loan balance exists in MCD's filings. |
| Other working capital | 0.8% of revenue change | judgment | Simple placeholder pending a full receivables, payables, and deferred-revenue schedule. |
| Minimum cash / revolver limit / rate | 500 / 5,000 / 4.5% | judgment | Liquidity safeguard and modelling placeholder; revise from debt-note and credit-agreement evidence. |
| Debt repayment / share buyback | 250 / 1,500 annually | judgment | Conservative fixed modelling choices, not management guidance. |
| Term-debt rate | 3.87% | history | FY2025 interest expense of $1,548M divided by $39,973M debt carrying value. |
| Cost of equity / terminal growth | 8.0% / 2.5% | judgment | Terminal growth is below the discount rate; both need a fuller market-input build for an investment conclusion. |
| Shares outstanding | 712.3M | fact | Latest diluted weighted-average shares in the June 2026 10-Q. |

## Result beside market price

The most recent completed market close available during this work was **$238.32 on September 23, 2026**. [Historical-price source](https://www.financecharts.com/stocks/MCD/summary/price) Run `python mcd_proforma.py` to print the model value, then compare it with this dated market price using the model's 712.3M diluted-share denominator. This is a valuation question, not a recommendation.

## Partner attack and response

**Attack:** Why assume a constant 19.0% SG&A/gross-profit ratio when the company is investing in technology and restaurant development?

**Response:** The ratio was stable in the calculated 2023–2025 history, so it is a transparent starting point rather than a claim that investment will not rise. I would change it if the next 10-K shows sustained SG&A growth faster than gross profit or if management identifies a recurring cost step-up that cannot be funded by system growth.

## AI-use disclosure

Codex helped locate filing sections, calculate the history ratios, and translate the labelled assumptions into `mcd_proforma.py`. I verified the cited 2025 revenue and inventory figures in the annual report; all non-filing forecasts are labelled as guidance or judgment rather than facts.
