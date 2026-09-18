# Lab 08 — McDonald's Peer P/E Comparison

## Decision and focused research question

**Target:** McDonald's Corporation (NYSE: MCD). **Comparison date:** September 10, 2026 close. **User:** long-only public-equity investor with no current position. **Question:** What is one MCD share worth at defensible peer P/E multiples, and how does that comparison differ from the saved Week 3 FCFF DCF?

McDonald's is primarily a franchisor: approximately 95% of its 46,028 restaurants were franchised at June 30, 2026. [MCD Q2 2026 10-Q, Business/MD&A](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm) Its FY2025 reported diluted EPS was positive at $11.95, so a P/E comparison is usable. [MCD 2025 10-K, EPS note](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm)

**What still needed research before calculation:** two public restaurant operators with similarly franchise-led economics; their FY2025 GAAP diluted EPS that was public by September 10, 2026; and September 10 closing prices on the same currency and per-share basis.

## Peer policy, written before selection

Include a candidate only if it is a public operating-company parent of global quick-service restaurant brands, derives material economics from franchise royalties/fees and related franchisee sales, reports positive annual GAAP diluted EPS, and has evidence public by the comparison date. Qualify candidates with material differences in brand mix, franchising percentage, company-operated exposure, geographic mix, capital structure, or discontinued-operation effects. Exclude a candidate if its business model is predominantly food production, grocery, delivery, or company-operated casual dining rather than a franchise-led restaurant system.

Evidence that would reject a candidate: negative annual GAAP EPS; an incompatible fiscal period or price date; lack of material franchise economics; or a one-time transaction/discontinued-operation item that makes reported EPS uninformative without a disclosed qualification.

## Candidate decisions and inputs

| Company | Decision | Business-model evidence and important difference | Price / date / source | FY2025 reported diluted EPS, fiscal year-end, publication | P/E |
|---|---|---|---:|---|---:|
| McDonald's (MCD), target | Target, not peer | Primarily franchisor; ~95% franchised at June 30, 2026. | $253.48, Sep. 10, 2026. [Historical price](https://www.financecharts.com/stocks/MCD/summary/price) | $11.95; year ended Dec. 31, 2025; Form 10-K filed Feb. 24, 2026. [10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm) | 21.211x |
| Yum! Brands (YUM) | **Use** | 97% of restaurants are operated by franchisees. [YUM 2025 10-K, Business/risk discussion](https://www.sec.gov/Archives/edgar/data/1041061/000104106126000084/yum-20251231.htm) Difference: YUM's KFC, Taco Bell, Pizza Hut and Habit portfolio is more franchise-heavy and has a different brand/geographic mix than MCD. | $143.89, Sep. 10, 2026. [Historical price](https://stockanalysis.com/stocks/yum/history/) | $5.55 GAAP; year ended Dec. 31, 2025; Form 10-K filed Feb. 20, 2026. [10-K, Consolidated Statements of Income](https://www.sec.gov/Archives/edgar/data/1041061/000104106126000084/yum-20251231.htm) | **25.926x** |
| Restaurant Brands International (QSR) | **Qualify, then use** | QSR had more than 95% franchised restaurants and derives franchise revenues primarily from royalties, fees, and related services. [QSR 2025 10-K, Business](https://www.sec.gov/Archives/edgar/data/1618756/000161875626000017/qsr-20251231.htm) Difference: its Tim Hortons, Burger King, Popeyes and Firehouse Subs mix includes more company-restaurant/refranchising and FY2025 discontinued-operation effects. | $76.49, Sep. 10, 2026. [Historical price](https://finance.yahoo.co.jp/quote/QSR/history) | $2.35 GAAP diluted EPS; year ended Dec. 31, 2025; Form 10-K signed Feb. 20, 2026. [10-K, Note 3—EPS](https://www.sec.gov/Archives/edgar/data/1618756/000161875626000017/qsr-20251231.htm) | **32.549x** |

All prices are USD closing prices on the same trading date. EPS is reported GAAP diluted EPS for the fiscal year ended December 31, 2025; it is not adjusted EPS, quarterly EPS, or an estimate.

## Calculator result and validation

`lab-08-pe.py` contains MCD, YUM, and QSR inputs; `lab-07-pe.py` remains the unchanged Asbury calculator. The Lab 08 calculator produces:

| Check | Result |
|---|---:|
| YUM hand check | $143.89 / $5.55 = **25.926x** |
| QSR P/E | $76.49 / $2.35 = **32.549x** |
| Peer median P/E | **29.238x** |
| MCD peer-implied range | **$309.82–$388.96** |
| MCD at peer median P/E | **$349.39** |
| Remove YUM | QSR-only reference estimate: **$388.96** (+$39.57 vs. full-peer median) |
| Remove QSR | YUM-only reference estimate: **$309.82** (−$39.57 vs. full-peer median) |

**Prediction and interpretation:** Removing QSR should lower the reference estimate because QSR has the higher P/E; the calculator confirms it falls from $349.39 to $309.82. Removing YUM raises it to $388.96. With either peer removed, the output is a single-peer reference, not a range. I retained QSR despite its qualifying differences because its franchise-led economics meet the policy and the disclosed discontinued-operation effect is named rather than hidden.

## DCF comparison and provisional call

| Method | MCD result and date | Main assumption or limitation |
|---|---:|---|
| Week 3 FCFF DCF | $193.20–$424.22 sensitivity range; base **$270.33** per share, September 10, 2026 | Starting FCFF $9.022B, 7.0% WACC, 2.5% terminal growth, and all reported cash treated as non-operating are estimates/assumptions. Terminal value is 81.3% of base enterprise value. See [Lab 6 inputs](lab-06-sources.md) and [DCF calculator](Lab%206%20Reverse%20dcf.py). |
| Peer P/E | **$309.82–$388.96**; median $349.39, September 10, 2026 | Two-peer range; YUM has a different brand portfolio and QSR's FY2025 GAAP EPS includes discontinued operations. P/E also incorporates each peer's capital structure and below-the-line items. |

The P/E range is above MCD's $253.48 comparison-date price, while the DCF base is only modestly above it. The difference is informative rather than an invitation to average: the peer method says the market paid higher P/E multiples for two franchise-led systems, whereas the DCF depends on MCD-specific FCFF normalization and discount-rate assumptions. The DCF is especially sensitive because terminal value dominates enterprise value.

**Provisional action: watch-defer.** Do not initiate solely from the two-peer P/E result. Initiate only if a refreshed DCF using a fully sourced WACC and a reconciled operating-cash assumption remains above the market price with a defined margin of safety, and the next results do not show a deterioration in franchisee/system sales or margin. The evidence most likely to change my mind is a sourced WACC/FCFF revision that moves the DCF base below the price, or a comparable-peer result that demonstrates the YUM/QSR premium is not transferable to MCD.

## Skeptical AI review and disposition

**Codex criticism:** The weakest supported link is transferring YUM and QSR P/E multiples directly to MCD with only two peers, particularly because QSR's FY2025 GAAP diluted EPS includes a discontinued-operation loss and MCD's capital structure differs. The question that could change the decision is: *After removing QSR's discontinued-operation effect or using a third policy-consistent franchisor, does the peer range still exceed MCD's market price?*

**Disposition: accept.** QSR's 10-K reports $2.63 diluted EPS from continuing operations, a $0.28 diluted loss from discontinued operations, and $2.35 total GAAP diluted EPS. [QSR 2025 10-K, Note 3](https://www.sec.gov/Archives/edgar/data/1618756/000161875626000017/qsr-20251231.htm) This confirms that the P/E comparison is usable but qualified and that a third sourced peer or continuing-operations normalization is the next robustness test; it does not justify silently changing the reported-EPS convention in this lab.



Codex helped locate filing sections, calculate P/E multiples, update the calculator, and draft this analysis. I retained only source-linked facts and kept FY2025 reported GAAP diluted EPS consistent across target and peers. Candidate selection, peer policy, qualifications, and the watch-defer judgment are presented for my review and ownership.
