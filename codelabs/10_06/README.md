# 10.06 — Run the SO-RSI Demo

The monitor reads real transfer failures before adding each observation to history, preventing the source demo’s self-recurrence error. It checks recurrence, reversal, predicted-versus-measured mismatch and regressions, then compares one naive proposal with one diagnosis-informed proposal under equal candidate budgets. Actual policy rejection is evidence; source-demo synthetic success rates are not reused. Monitor contract tests replay authentic SQL and do not generate taxi fixtures.

Source: [pinned lesson](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/02_second_order_diagnostics/step_01_run_demo/README.md). This is an original QueryForge adaptation, not a reproduction of the source paper's benchmark results.

## Reproduce

Prerequisites: complete M00–M03 and all preceding labs; `uv sync --locked`, authenticated Codex CLI, running Docker and checksum-verified TLC data. From the repository root:

```sh
uv run queryforge lab run 10.06
```

Implementation: [shared lesson code](../../src/queryforge/labs.py), [protected evaluator](../../src/queryforge/evaluator.py), [protocol](../../docs/evaluation-protocol.md). Input contracts are checked by the runnable lesson; failures stop execution rather than manufacture success. The output is [the actual JSON report](../../experiments/labs/10.06.json), which links the measurement or source evidence used. Read its interpretation together with the source-fidelity caveats. Missing source data, credentials or evidence is an error, not an offline simulation.

Video: deferred by owner until code verification and GitHub publication. No verified walkthrough link is claimed.
