# Results

The matched comparison evaluates four conditions and two seeds. Every run receives 12 search-candidate evaluations and one final two-task held-out evaluation after freezing. Incorrect held-out candidates contribute zero.

| Method | Seed | Search correct | Accepted generations | Held-out correct | Speedups | Geomean |
|---|---:|---:|---:|---:|---|---:|
| Fixed | 17 | 12/12 | 0 | 2/2 | 1.005, 1.016 | 1.011 |
| Fixed | 29 | 12/12 | 0 | 2/2 | 1.058, 0.994 | 1.026 |
| DREAM-RSI | 17 | 12/12 | 0 | 1/2 | 6.174, invalid | 0 |
| DREAM-RSI | 29 | 12/12 | 0 | 1/2 | 6.109, invalid | 0 |
| AIDE² adaptation | 17 | 12/12 | 0 | 1/2 | 6.075, invalid | 0 |
| AIDE² adaptation | 29 | 12/12 | 0 | 2/2 | 4.708, 0.317 | 1.222 |
| RSIFlow | 17 | 12/12 | 0 | 1/2 | 6.918, invalid | 0 |
| RSIFlow | 29 | 12/12 | 0 | 1/2 | 6.062, invalid | 0 |

No adaptive condition accepted an improver revision: no tested descendant reached the joint q01/q05 promotion rule. The experiment demonstrates real revision, inheritance, external testing and rollback, but **zero verified accepted recursive improvement** under this budget.

The fixed rules were correct on both held-out tasks in both seeds. AIDE² seed 29 had the largest nonzero held-out geomean, driven by q07 while q08 regressed heavily. The other adaptive runs generated invalid q08 SQL. Eight runs cannot establish comparative reliability.

The fixed condition uses deterministic rules after three provider timeouts blocked its model-backed seed 29. The earlier seed and timeouts are retained as attempts. This preserves equal SQL evaluation budgets but creates a proposal-compute difference disclosed in [threats](threats-to-validity.md).

Machine-readable source: [`comparison.json`](../experiments/reports/comparison.json).
