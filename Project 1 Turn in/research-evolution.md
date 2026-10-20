# Research Evolution - Project 1: McDonald's Corporation

## Edition A baseline

The unchanged Edition A baseline is preserved in `edition-a-unchanged.md`. It established an initial watch-defer position because a current share count, a completed intrinsic-value estimate, and a market-price comparison were still unresolved.

## Edition B - current decision

**Action: Watch-defer; do not initiate MCD at the September 23, 2026 reference price of $238.32.** The FCFF DCF base value is $183.15 per diluted share, with a $168.70 to $198.15 low/base/high range. The market price is above the high FCFF case.

| Changed item | Edition A | Edition B | Primary driver of change | Evidence or test that justified the change |
|---|---|---|---|---|
| Thesis/recommendation | Watch-defer because intrinsic value and a current market-price comparison were unresolved. | Watch-defer because the FCFF range remains below the market price, while peer methods disagree and require qualification. | Own analysis, course instruction, and AI-assisted organization/checking. | FCFF DCF, sensitivity output, reverse DCF, and separately reported peer cross-checks. |
| Data/source choice | FY2025 10-K was the main evidence base. | Added June 2026 10-Q, dated market-price evidence, and peer evidence. | Research plan and own analysis. | Filing locators and valuation-source map. |
| Assumption/model design | Planned a DCF and enterprise-to-equity bridge. | Built a five-year FCFF model with balance/cash-flow checks, sensitivity analysis, reverse DCF, and a bounded workbench. | Course instruction and own model work, with AI-assisted code drafting and debugging. | Synthetic known-answer reconciliation, balance checks, cash-flow ties, monotonicity checks, and changed-input run. |
| Risk, limitation, or uncertainty | WACC, terminal growth, debt/cash, share count, and normalized cash flow were unresolved. | Those remain material; terminal-value dependence and peer-definition differences are now explicit limitations. | Own analysis and validation. | Terminal value is 81.3% of base EV; peer-method differences are preserved rather than averaged. |

## What changed from Edition A to Edition B, and why?

The recommendation stayed watch-defer, but the reason became more specific. Edition A had not completed the valuation. Edition B produces an FCFF range below the reference market price, identifies the sensitivity to growth and terminal assumptions, and preserves the disagreement with peer methods instead of selecting the most favorable output. This evidence supports deferring action until stronger primary evidence supports higher sustainable growth or margins, lower capex needs, or a lower supportable discount rate.

## Material AI-output check

One AI-assisted suggestion was to use peer P/E evidence as a cross-check beside the FCFF DCF. I **qualified** that suggestion after checking the peer evidence. P/E and FCFF do not value the same object in the same way: P/E includes peer capital structure and below-the-line earnings, while FCFF values operating cash flows and then explicitly bridges debt and excess cash. In addition, the small P/E sample includes QSR, which has a discontinued-operations issue. The result is presented as a qualified cross-check, not averaged into the DCF.
