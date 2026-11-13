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
