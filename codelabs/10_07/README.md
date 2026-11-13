# 10.07 — Analyze Diagnostic Probes

The lesson counts observed anomaly types, inspects SQL operators, policy errors, result schemas and repeated timings, and reruns the actual naive and diagnostic candidates. Recommendations distinguish a confirmed language-policy rejection from unproven causal explanations of latency. No recurrence or reversal is invented when the trace contains none. The report includes all probe outputs and the fresh evaluator ID.

Source: [pinned lesson](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/02_second_order_diagnostics/step_02_analyze_probes/README.md). This is an original QueryForge adaptation, not a reproduction of the source paper's benchmark results.

## Reproduce

Prerequisites: complete M00–M03 and all preceding labs; `uv sync --locked`, authenticated Codex CLI, running Docker and checksum-verified TLC data. From the repository root:

```sh
uv run queryforge lab run 10.07
```

Implementation: [shared lesson code](../../src/queryforge/labs.py), [protected evaluator](../../src/queryforge/evaluator.py), [protocol](../../docs/evaluation-protocol.md). Input contracts are checked by the runnable lesson; failures stop execution rather than manufacture success. The output is [the actual JSON report](../../experiments/labs/10.07.json), which links the measurement or source evidence used. Read its interpretation together with the source-fidelity caveats. Missing source data, credentials or evidence is an error, not an offline simulation.

Video: deferred by owner until code verification and GitHub publication. No verified walkthrough link is claimed.
