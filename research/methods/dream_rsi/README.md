# DREAM-RSI adaptation

QueryForge adapts DREAM-RSI's online exploration → accumulated discovery tree → offline policy rewrite → fresh online rollout mechanism. It uses the pinned Google Research source at commit `8ec35bd2538220517ce1bfca4282db21b8c518db` as the mechanism reference. It does not reproduce the paper's benchmark, replay fitness, parallel planner, or reported results.

```text
I0 proposes 4 SQL candidates → protected evaluation
tree history → model rewrites exploration policy I1
I1 proposes a fresh batch → accept only if q01 and q05 each reach 1.02×
repeat once → freeze accepted policy → one q07/q08 held-out evaluation
```

The outer rewrite procedure, model, task definitions, budget and protected evaluator remain fixed. A proposed policy is used in the next fresh generation before acceptance; failed descendants roll back. The two real seeds accepted zero policy revisions. Both final runs produced a correct fast q07 candidate and an incorrect q08 candidate, so held-out correctness failed and no recursive improvement is claimed.

Evidence: [`dream-rsi-seed-17.json`](../../../experiments/methods/dream-rsi-seed-17.json), [`dream-rsi-seed-29.json`](../../../experiments/methods/dream-rsi-seed-29.json). Implementation: [`methods.py`](../../../src/queryforge/methods.py). Video upload is pending owner production.
