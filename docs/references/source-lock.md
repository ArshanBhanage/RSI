# Source lock

Course commit: `fabd4c79207df6a6a144c22fb1703fc074a048e7`. Inspected 2026-11-06 (America/Los_Angeles).

The machine-readable lock records exact SHA-256 hashes and immutable download URLs. Recheck with `python3 scripts/verify_sources.py`. This checks source integrity, not experimental success.

| Lab | Upstream title | Immutable source |
|---|---|---|
| 10.01 | Distinguish Claim from Evidence | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/00_reading_frontier_research/step_01_claim_vs_evidence/README.md) |
| 10.02 | Audit an October 2026 Paper | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/00_reading_frontier_research/step_02_audit_paper/README.md) |
| 10.03 | Run the Budget RSI Demo | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/01_budget_rsi_scoring/step_01_run_demo/README.md) |
| 10.04 | Analyze the Scoring Mechanism | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/01_budget_rsi_scoring/step_02_analyze_mechanism/README.md) |
| 10.05 | Extend to Your Own Edits | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/01_budget_rsi_scoring/step_03_extend/README.md) |
| 10.06 | Run the SO-RSI Demo | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/02_second_order_diagnostics/step_01_run_demo/README.md) |
| 10.07 | Analyze Diagnostic Probes | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/02_second_order_diagnostics/step_02_analyze_probes/README.md) |
| 10.08 | Apply to Debugging Task | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/02_second_order_diagnostics/step_03_apply/README.md) |
| 10.09 | Compare Scaling Approaches | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/03_scaling_coordination/step_01_compare/README.md) |
| 10.10 | Simulate Leader-Follower Coordination | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/03_scaling_coordination/step_02_simulate/README.md) |
| 10.11 | Simulate Swarm Evolution | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/03_scaling_coordination/step_03_swarm/README.md) |
| 10.12 | Compare Workflow Adaptation | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/04_adaptive_workflows/step_01_compare/README.md) |
| 10.13 | Simulate RSIFlow Meta-Agent | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/04_adaptive_workflows/step_02_rsiflow/README.md) |
| 10.14 | Simulate Self-HPO Alternation | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/04_adaptive_workflows/step_03_selfhpo/README.md) |
| 10.15 | Calculate RSI-Index | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/05_environments_metrics/step_01_rsi_index/README.md) |
| 10.16 | Compare Environments | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/05_environments_metrics/step_02_environments/README.md) |
| 10.17 | Analyze Metrics | [README](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/10_research_studio/05_environments_metrics/step_03_metrics/README.md) |

## Reconciliation

All 17 IDs are present in six groups. Theme 11 is separate. The requested original `rsi/COURSE-MAP.md` path is absent at this commit; the root map is present. Several upstream labs explicitly request toy simulations. This assignment instead requires real SQL executions and measured outcomes, preserving the lesson objective while increasing implementation scope.

## Source defects to resolve before implementation

- Lab 10.15 prints `(initial-final)/(ideal-initial)` but calculates `(final-initial)/(ideal-initial)` in its example. Verify the original RSIGym definition at L10.15; neither sign is adopted here.
- The Budget demo samples synthetic features/outcomes and prints assumed cost savings. Its selector describes Thompson sampling but implements proportional sampling. It is not benchmark evidence.
- SO-RSI assigns different success probabilities to the two approaches. Its monitor appends the current trace before recurrence/opposing checks, so recurrence can compare a trace with itself and opposing checks inspect the current trace. Do not port this as a tested diagnostic engine.
- Some relative next/group links resolve incorrectly from their source directories. Use the canonical paths in this lock rather than copying those links.

Source files are downloaded to a gitignored cache; upstream course prose is not vendored.
