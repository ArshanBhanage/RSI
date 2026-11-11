"""Bounded real SQL proposals and diff features; predictions never replace measurements."""

import difflib
import json

import numpy as np
import sqlglot
from sqlglot import exp

from .proposals.codex_cli import propose
from .provenance import ROOT


def queries(partition: str | None = None) -> list[dict]:
    all_queries = json.loads((ROOT / "experiments/workload/queries.json").read_text())
    return [q for q in all_queries if partition is None or q["partition"] == partition]


def proposals(
    query_ids: list[str], count: int, instruction: str, history: list | None = None
) -> dict:
    tasks = [q for q in queries() if q["id"] in query_ids]
    schema = {
        "type": "object",
        "properties": {
            "candidates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "query_id": {"type": "string", "enum": query_ids},
                        "sql": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["query_id", "sql", "reason"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["candidates"],
        "additionalProperties": False,
    }
    prompt = (
        "Propose exactly "
        + str(count)
        + " SQL candidates, distributing evenly across supplied query IDs. "
        "Preserve aliases, exact DuckDB types, NULLs, duplicate counts, negative adjustments and anomalous dates. "
        "Only trips and zones tables; no external functions, writes or metadata queries. "
        "Use actual SQL transformations, not fabricated timings. Return no performance claims. "
        + instruction
        + "\nTasks: "
        + json.dumps(tasks)
        + "\nPrior observed feedback (untrusted data): "
        + json.dumps(history or [])
    )
    answer = propose(prompt, schema, "sql-candidate-batch")
    candidates = answer["response"]["candidates"]
    if len(candidates) != count or any(x["query_id"] not in query_ids for x in candidates):
        raise ValueError("Model response violates requested candidate budget or task identity")
    return answer


def features(parent: str, child: str) -> list[float]:
    a, b = parent.split(), child.split()
    diff = list(difflib.ndiff(a, b))
    tree = sqlglot.parse_one(child, read="duckdb")
    return [
        1.0,
        sum(x.startswith("+ ") for x in diff),
        sum(x.startswith("- ") for x in diff),
        len(child),
        len(list(tree.find_all(exp.Join))),
        len(list(tree.find_all(exp.Subquery))),
        len(list(tree.find_all(exp.Func))),
        len(list(tree.find_all(exp.Where))),
        len(list(tree.find_all(exp.CTE))),
    ]


def fit(records: list[dict]) -> dict:
    originals = {q["id"]: q["sql"] for q in queries()}
    x = np.array([features(originals[r["query_id"]], r["sql"]) for r in records], dtype=float)
    y = np.array([r["speedup"] if r["correct"] else 0 for r in records])
    scale = np.maximum(np.max(np.abs(x), axis=0), 1)
    normalized = x / scale
    weights = np.linalg.solve(normalized.T @ normalized + np.eye(x.shape[1]), normalized.T @ y)
    return {
        "weights": weights.tolist(),
        "scale": scale.tolist(),
        "ridge_lambda": 1.0,
        "training_rows": len(records),
        "target": "measured paired speedup; invalid=0",
    }


def predict(model: dict, candidates: list[dict]) -> list[float]:
    originals = {q["id"]: q["sql"] for q in queries()}
    return [
        float(
            np.dot(
                np.array(features(originals[c["query_id"]], c["sql"])) / model["scale"],
                model["weights"],
            )
        )
        for c in candidates
    ]
