"""Gap normalization with explicit metric direction and undefined-ceiling handling."""

import json
import math

from .provenance import ROOT


def gap_closed(initial: float, final: float, ideal: float = 1.0) -> float | None:
    if not all(math.isfinite(x) for x in [initial, final, ideal]):
        raise ValueError("Non-finite score")
    if ideal == initial:
        return None
    return (final - initial) / (ideal - initial)


def index_lab() -> dict:
    ledger = [
        json.loads(line)
        for line in (ROOT / "experiments/runs/evaluations.jsonl").read_text().splitlines()
    ]
    latest = {}
    for event in ledger:
        if event["final"] or "security" in event["method"]:
            continue
        for row in event["records"]:
            latest[row["query_id"]] = (event["id"], row)
    rows = []
    for qid, (event_id, row) in sorted(latest.items()):
        utility = row["speedup"] / (1 + row["speedup"]) if row["correct"] else 0
        rows.append(
            {
                "query_id": qid,
                "evaluation_id": event_id,
                "correct": row["correct"],
                "speedup": row["speedup"],
                "initial_correctness": 1.0,
                "final_correctness": float(row["correct"]),
                "correctness_gap_closed": gap_closed(1, float(row["correct"])),
                "baseline_sql_utility": 0.5,
                "candidate_sql_utility": utility,
                "sql_utility_gap_closed": gap_closed(0.5, utility),
            }
        )
    return {
        "source": "https://arxiv.org/html/2610.10310#S4.SS2",
        "paper_equation": "mean((final - initial)/(1 - initial))",
        "course_correction": "The course formula reverses the numerator; its worked example and the primary paper use final minus initial.",
        "selection_rule": "Latest observed nonsecurity record for every observed development/selection task, not the best observed record.",
        "rows": rows,
        "official_accuracy_index": None,
        "undefined_reason": "All protected reference tasks start at correctness one, so the remaining correctness gap is zero. A finite accuracy RSI-Index cannot be reported.",
        "sql_utility_index": sum(r["sql_utility_gap_closed"] for r in rows) / len(rows),
        "utility_definition": "correct ? speedup/(1+speedup) : 0; baseline utility=0.5, ceiling=1",
        "interpretation": "SQL utility normalization is our explicit latency adaptation, not the paper benchmark index or evidence of recursive gain. Latest observations are descriptive, not selected final systems. Negative values are preserved.",
    }


def metrics_audit() -> dict:
    labs = [
        json.loads((ROOT / "experiments/labs" / f"10.{number:02d}.json").read_text())
        for number in range(1, 17)
    ]
    ledger = [
        json.loads(line)
        for line in (ROOT / "experiments/runs/evaluations.jsonl").read_text().splitlines()
    ]
    evaluation_ids = {row["id"] for row in ledger}
    proposal_ids = {
        path.parent.name for path in (ROOT / "experiments/proposals").glob("*/response.json")
    }
    referenced_evaluations: set[str] = set()
    referenced_proposals: set[str] = set()

    def walk(value) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"evaluation_id", "source_evaluation"} and isinstance(item, str):
                    referenced_evaluations.add(item)
                if key.endswith("proposal_id") and isinstance(item, str):
                    referenced_proposals.add(item)
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    for lab in labs:
        walk(lab)
    expected_negative_ids = {"nonexistent-test-id"}
    missing_evaluations = sorted(referenced_evaluations - evaluation_ids - expected_negative_ids)
    missing_proposals = sorted(referenced_proposals - proposal_ids)
    assert not missing_evaluations and not missing_proposals
    return {
        "audited_labs": [lab["lab_id"] for lab in labs],
        "ledger_events": len(ledger),
        "referenced_evaluations": len(referenced_evaluations),
        "referenced_proposals": len(referenced_proposals),
        "missing_evaluations": missing_evaluations,
        "missing_proposals": missing_proposals,
        "intentional_negative_references": sorted(referenced_evaluations & expected_negative_ids),
        "metrics": {
            "RSI-Index": {
                "problem": "Normalize fractions of remaining score gaps.",
                "use": "Comparable reward benchmarks with a meaningful ceiling.",
                "limit": "Undefined at a saturated initial score; inheritance and cost are separate.",
            },
            "steering-split solve rate": {
                "problem": "Select candidates without held-out labels.",
                "use": "A representative predeclared proxy split.",
                "limit": "Proxy overfitting and multiplicity remain.",
            },
            "recursive learnability": {
                "problem": "Choose informative self-play tasks as skills change.",
                "use": "Controlled orchestration rollouts with skill withdrawal.",
                "limit": "Cannot be inferred from one static score.",
            },
            "swarm diversity": {
                "problem": "Track distinct hypotheses and components.",
                "use": "Population search with externally tested descendants.",
                "limit": "Diversity alone does not imply correctness or gain.",
            },
        },
        "interpretation": "Cross-artifact integrity audit over sixteen real reports. Metrics answer different questions; none alone demonstrates recursive self-improvement.",
    }
