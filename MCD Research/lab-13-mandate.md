# Lab 13 — Meridian Foundation Reserve

## S1–S10 classification — complete without AI

| Statement | Your classification | Your one-line reason |
|---|---|---|
| S1 — Horizon seven years; annual rebalancing. | Hard constraint | The seven-year horizon sets the decision period, and annual rebalancing is an operational trading rule. |
| S2 — Objective: CPI + 4% a year, net of costs, over rolling five-year periods. | Objective | It states the return outcome the reserve is intended to achieve, including measurement period and costs. |
| S3 — Pays out $0.75M every quarter; twelve months of payouts held in cash or daily-liquid government securities. | Hard constraint | It requires a specific amount and form of liquidity for scheduled distributions. |
| S4 — Benchmark: 60% global equities, 40% U.S. investment-grade bonds. | Preference | It is a performance comparison reference, not a stated allocation requirement or investability rule. |
| S5 — Long-only: no borrowing, short sales or derivatives. | Hard constraint | It explicitly forbids specified portfolio positions and financing tools. |
| S6 — No single issuer above 8%. | Hard constraint | It is a measurable issuer-concentration ceiling. |
| S7 — Annual turnover at most 25% without committee approval. | Hard constraint | It sets a measurable trading limit, subject only to the stated approval exception. |
| S8 — At least 90% redeemable within five business days. | Hard constraint | It gives a measurable minimum liquidity percentage and a defined redemption window. |
| S9 — “The reserve cannot have a calendar-year loss greater than 10%.” No measure, no breach rule. | Unverifiable promise | No return measure, valuation timing, or breach-and-remedy rule is defined, so it cannot yet be coded or tested consistently. |
| S10 — No sector, ESG, tax or home-bias preference; nobody has said what the pilot should optimize. | Missing | The absence of preferences does not tell the optimizer what risk or portfolio characteristic to optimize. |

## Checker evidence

Run:

```powershell
python .\mandate.py
```

The expected checkable-rule verdicts are A: pass; B: fails 3 rules; C: fails 1 rule; D: pass. Candidate D holds 3% cash, 87% Treasury bills, and 10% global equity index fund.

## Candidate D — AI attack and judgment

Candidate D passes every checkable rule but could still be rejected because its 90% cash/Treasury allocation may make the CPI + 4% rolling-five-year objective implausible. It exposes S2: the CIO must state the required probability of meeting the return objective, or an acceptable risk/return trade-off, before an optimizer can choose a portfolio.

## Your question for the CIO

**Question:** What risk objective should govern optimization—specifically, what probability of achieving CPI + 4% over rolling five-year periods is acceptable, and what calendar-year loss measure and remedy should apply if that objective conflicts with the loss limit?

**Answer that would change the portfolio:** If the CIO prioritizes a high probability of meeting CPI + 4%, the allocation should hold materially more growth assets than candidate D. If the CIO instead treats avoiding a calendar-year loss beyond 10% as the binding objective, the portfolio should use a more conservative risk budget and an explicitly defined downside-control approach.

## Reflection

1. A checker can only test rules that have numerical definitions. Candidate D passes liquidity, concentration, long-only, and reserve rules, but its 90% cash/Treasury allocation may be poorly suited to achieving CPI + 4%; a mechanically compliant portfolio can therefore conflict with the client’s unstated risk-return priorities.

2. S4 was the least certain classification because a benchmark is important for evaluating performance but does not by itself require a particular portfolio allocation. I classified it as a preference/reference rather than a hard portfolio constraint.

3. In an investment policy statement, S1 defines time horizon and rebalancing governance; S2 is the return objective; S3 and S8 are liquidity constraints; S4 is the benchmark; S5–S7 are implementation, concentration, and turnover constraints; S9 is an inadequately specified risk constraint; and S10 identifies the missing optimization/risk-priority decision. Together, these statements show that an IPS must translate client language into objectives, measurable constraints, governance rules, and decision criteria before a portfolio is optimized.
