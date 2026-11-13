# 10.11 — Simulate Swarm Evolution

Five real researcher calls explore distinct SQL hypotheses. Measured evidence selects two parents; subsequent model calls generate a feedback-guided mutation and a component recombination, each evaluated on authentic taxi data. Parent indexes, proposal rationales, failures and complete evaluation records are preserved. Population evolution is demonstrated without claiming that SQL changes alone establish recursive improvement of the search procedure.

Source: [pinned lesson](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/03_scaling_coordination/step_03_swarm/README.md). This is an original QueryForge adaptation, not a reproduction of the source paper's benchmark results.

## Reproduce

Prerequisites: complete M00–M03 and all preceding labs; `uv sync --locked`, authenticated Codex CLI, running Docker and checksum-verified TLC data. From the repository root:

```sh
uv run queryforge lab run 10.11
```

Implementation: [shared lesson code](../../src/queryforge/labs.py), [protected evaluator](../../src/queryforge/evaluator.py), [protocol](../../docs/evaluation-protocol.md). Input contracts are checked by the runnable lesson; failures stop execution rather than manufacture success. The output is [the actual JSON report](../../experiments/labs/10.11.json), which links the measurement or source evidence used. Read its interpretation together with the source-fidelity caveats. Missing source data, credentials or evidence is an error, not an offline simulation.

Video: deferred by owner until code verification and GitHub publication. No verified walkthrough link is claimed.
