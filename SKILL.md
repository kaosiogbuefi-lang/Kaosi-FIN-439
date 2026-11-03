---
name: buffett-10k
description: Analyze a public company's last five annual 10-K facts with Buffett-style operating checks when the user asks for a price-free long-term business-quality screen.
---

# Buffett 10-K Screen

Use `scripts/buffett_10k.py` to obtain the numbers. Do not estimate a missing value, use price data, or substitute a non-10-K filing.

1. Set `SEC_USER_AGENT` to the user's name and email, then run `python scripts/buffett_10k.py TICKER`.
2. Base every numeric statement in the memo only on the script output. If a source value, ROE, owner earnings, or a check says `not found` or `not known`, say so rather than filling the gap.
3. Write a short Markdown memo saved as `TICKER_buffett_memo.md`. Judge the business only: choose **own the business**, **watch it**, or **pass**; do not discuss market price.
4. State why the deterministic checks support or limit the judgment. The model supplies the judgment; the script supplies all numbers.

The Streamlit companion app is `buffett_app.py` in the coursework workspace. It independently flags numbers in the memo that the script did not print.
