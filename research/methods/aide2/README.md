# AIDE²-inspired harness evolution

No exact official end-to-end AIDE² implementation was identified in the pinned paper and author material. QueryForge therefore labels this an original adaptation. The predecessor `WecoAI/aideml` is not represented as AIDE².

An outer, fixed model procedure proposes a descendant research harness containing an executable candidate instruction and preflight/deduplication flags. The descendant controls the next fresh SQL generation. The protected evaluator and the promotion rule remain outside the harness: both q01 and q05 must be correct and reach at least 1.02×. Rejected descendants roll back before the next revision.

Across seeds 17 and 29, zero descendants met the joint promotion rule. Seed 17's q08 transfer was incorrect; seed 29's two held-out candidates were correct, with q07 faster and q08 slower. These are failed/limited search outcomes, not evidence that the harness recursively improved.

Evidence: [`aide2-seed-17.json`](../../../experiments/methods/aide2-seed-17.json), [`aide2-seed-29.json`](../../../experiments/methods/aide2-seed-29.json). Implementation: [`methods.py`](../../../src/queryforge/methods.py). Video upload is pending owner production.
