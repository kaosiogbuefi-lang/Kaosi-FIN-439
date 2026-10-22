# Lab 15 — Price sources and universe

## Universe

| Ticker | Fund role | Reserve-eligible? |
|---|---|---|
| BIL | Treasury-bill fund | Yes |
| IEF | 7–10 year Treasury-note fund | Yes |
| LQD | Investment-grade corporate-bond fund | No |
| VT | Global-equity fund | No |

The objective is 6.5% expected return. The hard constraint is at least 3% in BIL and/or IEF.

## Price data

`prices.csv` contains the monthly Yahoo Finance **Adjusted Close** values supplied from the historical-data pages on 2026-10-22. It covers 2021-11 through 2026-10, is oldest first, and has one column per ticker. These historical averages are estimates, not forecasts.

- [BIL history](https://finance.yahoo.com/quote/BIL/history/)
- [IEF history](https://finance.yahoo.com/quote/IEF/history/)
- [LQD history](https://finance.yahoo.com/quote/LQD/history/)
- [VT history](https://finance.yahoo.com/quote/VT/history/)

## App results

The app used a 6.5% expected-return objective and a 3% minimum reserve-eligible weight, with BIL and IEF marked reserve-eligible.

| Estimation window | BIL | IEF | LQD | VT | Expected return | Volatility | Reserve-eligible weight |
|---|---:|---:|---:|---:|---:|---:|---:|
| All monthly observations | 60.0% | 0.0% | 0.0% | 40.0% | 6.90% | 6.01% | 60.0% |
| Last 36 monthly observations | 85.0% | 0.0% | 0.0% | 15.0% | 6.87% | 1.76% | 85.0% |

The largest weight change is 25 percentage points: BIL rises from 60.0% to 85.0%, while VT falls from 40.0% to 15.0%.
