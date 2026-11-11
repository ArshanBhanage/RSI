# Method fidelity at M00

No method has been executed. This table records source-supported mechanisms and intended adaptations, not completed implementations or reproduced performance.

| Method | Source and release | Changed object / inheritance | QueryForge boundary |
|---|---|---|---|
| DREAM-RSI | [Paper v2](https://arxiv.org/abs/2609.14858v2), submitted September 14, revised October 6, 2026; [code](https://github.com/google-research/dream-rsi/tree/8ec35bd2538220517ce1bfca4282db21b8c518db) | Exploration policy rewritten against accumulated replay trees; selected policy controls a fresh online round. Base coding agent and evaluator stay fixed. | Use the custom task interface with protected SQL evaluation; replay estimates cannot establish unseen online gains. No mathematical or GPU benchmark reproduction is claimed. |
| AIDE² | [Paper v1](https://arxiv.org/abs/2609.26457v1), submitted September 22, 2026; [authors' report](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement) | An outer optimizer edits an inner research harness, evaluates it externally and retains successful descendants for later edits. | An original AIDE²-inspired adaptation is required. No official complete AIDE² release was identified in the inspected paper/report. This is a bounded search finding, not proof that no release exists. |
| RSIFlow | [Paper v2](https://arxiv.org/abs/2610.21791v2), submitted October 15, revised November 2, 2026; [code](https://github.com/1HUAN1/RSI-Flow/tree/496d3cfb9ff39997d107d0ff29e746b07e638180) | A persistent Meta controller chooses task components to improve and retains intervention evidence as skills. | Released code keeps the executable Meta program fixed. Any executable Meta evolution is a separately labeled educational extension. CPU SQL experiments cannot reproduce the Qwen/GPU training study. |

## Licensing and source availability

- DREAM-RSI's pinned core is Apache-2.0. Its third-party KernelBench files are separately licensed, and downloaded SimpleTES tasks are AGPL-3.0. QueryForge must supply its own task rather than import those benchmark tasks accidentally.
- RSIFlow's root license is MIT, with third-party notices and separately licensed evaluator assets. Preserve relevant notices if incorporating source. External models, datasets and GPU services are not bundled.
- The course is MIT licensed. Only hashes, links and original explanations are included here.
- `kudoej/dream-rsi` HEAD was `4149ea9181ab1db80f85717ffda2c9f0f130e85b`; it is a separate project repository, not the pinned executable source.
- `WecoAI/aideml` HEAD was `ad73d227af481bea3de06f884f41b2993dd6453a`. This is the predecessor AIDE, not evidence of an AIDE² release. Its source is not incorporated.

## Original problem

QueryForge asks whether revising the search policy or harness improves the efficiency of correctness-preserving SQL search under equal evaluation budgets. The target is analytical SQL over authentic NYC TLC records; the improver chooses and validates candidate rewrites; the meta-improver revises that procedure for a later generation. Only external, frozen evaluation can authorize promotion.

The [official TLC source](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) provides monthly Parquet records and zone metadata. It warns that provider-submitted trip data are not guaranteed accurate. M02 must verify specific 2025 downloads and semantics; M00 does not claim data ingestion, row counts or latency results.
