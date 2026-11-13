# 10.12 — Compare Workflow Adaptation

The source-grounded comparison identifies RSIFlow bottleneck routing and released fixed-Meta skill evolution, versus Self-HPO alternating harness search and reinforcement learning of policy weights. The runnable audit checks actual two-generation workflow and conditional-memory trajectories and links their evaluator IDs. QueryForge does not claim model-weight training or use either paper’s scores as its own.

Source: [pinned lesson](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/04_adaptive_workflows/step_01_compare/README.md). This is an original QueryForge adaptation, not a reproduction of the source paper's benchmark results.

## Reproduce

Prerequisites: complete M00–M03 and all preceding labs; `uv sync --locked`, authenticated Codex CLI, running Docker and checksum-verified TLC data. From the repository root:

```sh
uv run queryforge lab run 10.12
```

Implementation: [shared lesson code](../../src/queryforge/labs.py), [protected evaluator](../../src/queryforge/evaluator.py), [protocol](../../docs/evaluation-protocol.md). Input contracts are checked by the runnable lesson; failures stop execution rather than manufacture success. The output is [the actual JSON report](../../experiments/labs/10.12.json), which links the measurement or source evidence used. Read its interpretation together with the source-fidelity caveats. Missing source data, credentials or evidence is an error, not an offline simulation.

Video: deferred by owner until code verification and GitHub publication. No verified walkthrough link is claimed.
