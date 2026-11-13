"""Measured coordination adaptations: scoped findings and bounded real worker calls."""

import json

from .evaluator import evaluate
from .provenance import ROOT


def comparison() -> dict:
    calibration = json.loads((ROOT / "experiments/labs/10.03.json").read_text())["result"]
    candidates = []
    choices = []
    for query_id in ["q01", "q02"]:
        rows = [r for r in calibration["records"] if r["query_id"] == query_id]
        leader = max(rows, key=lambda r: r["speedup"] if r["correct"] else 0)
        for strategy, row in [("evidence_guided", leader), ("first_proposal", rows[0])]:
            candidates.append({"query_id": query_id, "sql": row["sql"]})
            choices.append({"strategy": strategy, "query_id": query_id})
    actual = evaluate(candidates, "lab-10.09-coordination-selection")
    return {
        "source_evaluation": calibration["evaluation_id"],
        "choices": choices,
        "evaluation_id": actual["id"],
        "records": actual["records"],
        "comparison": {
            "AReaL-RSI": {
                "source": "https://arxiv.org/abs/2610.18083",
                "mechanism": "Leader-directed specialist investigation with conditionally shared resolved/unresolved findings and campaign review.",
                "advantage": "Preserves applicability conditions for persistent research objectives.",
                "limitation": "Coordination overhead and mistaken leader orientations consume whole-system resources.",
                "use": "Persistent programs with separable specialist work and comparable external evaluation.",
            },
            "SwarmRSI": {
                "source": "https://arxiv.org/abs/2610.20431",
                "mechanism": "Feedback-guided mutation of hypotheses and implementations, plus complementary component recombination.",
                "advantage": "Can retain useful partial components even when a complete program is weak.",
                "limitation": "Components may be incompatible; recombination still requires external validation.",
                "use": "Diverse hypotheses with reusable implementation components.",
            },
        },
        "interpretation": "Source-grounded mechanism comparison and a small fresh evaluation of retrospective selection choices. This is not an AReaL/Swarm system-level benchmark; each arm evaluates two candidates, and prior calibration costs are shared and disclosed.",
    }
