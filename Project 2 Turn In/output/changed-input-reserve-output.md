# Locked Changed-Input Output — 2026-11-23 Reserve Minimum

## Freeze and execution boundary

The prediction was committed and pushed before this scenario was run:

- Prediction commit: [`6dec567a2e51f8f0709d1d58fc2b50a5d1cf31c9`](https://github.com/kaosiogbuefi-lang/Kaosi-FIN-439/commit/6dec567a2e51f8f0709d1d58fc2b50a5d1cf31c9)
- Git commit timestamp: `2026-11-23T18:29:38-06:00`
- Runner: `python changed_input_reserve_test.py`
- AI assistance: instructor-authorized ChatGPT/Codex assistance, as communicated by the student. This is not described as an AI-off or human-only validation.

## Inputs

| Input | Baseline | Changed |
|---|---:|---:|
| Estimated annual net-return objective | 6.50% | 6.50% |
| BIL-plus-IEF reserve minimum | 3.0% | 90.0% |
| Illustrative annual cost | 0 bp | 0 bp |
| Price data and estimation windows | Default `prices.csv`; all months and final 36 returns | Unchanged |
| DGS10 condition | Verified ALFRED vintage | Unchanged |

## Prediction made before execution

Both searches would be infeasible because a 90% reserve minimum permits at most 10% in the higher-return non-reserve sleeve. The process would return `Reject`, no allocation range, and no allocation-movement comparison without crashing.

## Actual console output

```text
Changed input: reserve minimum from 3.0% to 90.0%
All-months base window: no feasible mix meets the 6.50% net-return objective and 90.0% reserve minimum.
Last-36-returns stress window: no feasible mix meets the 6.50% net-return objective and 90.0% reserve minimum.
Recommendation: Reject
Reason: Reject the process because the base allocation fails: no feasible base portfolio.
```

## Comparison and interpretation

| Criterion fixed before execution | Actual result | Comparison |
|---|---|---|
| All-month base is infeasible | Infeasible | Matched |
| Last-36-return stress is infeasible | Infeasible | Matched |
| Action is `Reject` | `Reject` | Matched |
| No executable range | Central recommendation logic returns `allocation_range: None` when the base is infeasible | Matched |
| No crash | Script exited normally | Matched |

There was no difference between the predicted and actual direction or decision. The result does **not** alter the default scenario or investment methodology; it demonstrates that the existing feasibility gate refuses an overly restrictive reserve requirement rather than producing a misleading allocation.
