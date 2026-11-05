---
name: cathie-wood-10k
description: Screen a public company's last five annual 10-K facts for Cathie Wood-style revenue growth and R&D intensity without using price data.
---

# Cathie Wood 10-K Screen

Run `scripts/buffett_10k.py TICKER` for the facts and checks. It is the shared deterministic engine for the legend panel.

- Use only values printed by the script in the memo. Do not estimate a missing value or replace a 10-K fact with another filing.
- The revenue-growth threshold is 15% per year. Keep it unless a deliberate threshold probe is requested, then restore it.
- Write `TICKER_cathie_wood_memo.md`: choose **own the business**, **watch it**, or **pass** based on the printed checks only. Judge the business, not its market price.
- Preserve `not found` and `not known` in the memo. The app audits every memo number against the script output.
