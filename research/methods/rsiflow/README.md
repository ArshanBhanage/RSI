# RSIFlow adaptation

This implementation follows the public release boundary: a fixed executable Meta controller diagnoses measured trajectories, chooses a component-specific workflow and writes conditional improvement memory. It does not describe the educational extension as official executable Meta-program evolution, and it does not reproduce the paper's GPU/model-training experiments.

Each revision receives only actual correctness, error and speed observations. Its instruction and routing flags govern the next fresh generation. External acceptance requires correct best candidates reaching 1.02× on both q01 and q05. Rejected skills remain in lineage but are not retrieved as supported memory.

Across both seeds, no workflow/skill revision met the joint promotion rule. Both held-out runs produced a correct faster q07 candidate and an incorrect q08 candidate. The correct conclusion is zero verified accepted recursive improvement under this budget.

Evidence: [`rsiflow-seed-17.json`](../../../experiments/methods/rsiflow-seed-17.json), [`rsiflow-seed-29.json`](../../../experiments/methods/rsiflow-seed-29.json). Implementation: [`methods.py`](../../../src/queryforge/methods.py). Video upload is pending owner production.
