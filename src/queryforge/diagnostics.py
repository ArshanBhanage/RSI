"""Trace-derived anomaly detection; compare with history before appending a new event."""

import hashlib

import sqlglot


def fingerprint(sql: str) -> str:
    normalized = sqlglot.parse_one(sql, read="duckdb").sql(dialect="duckdb")
    return hashlib.sha256(normalized.encode()).hexdigest()


def inspect(record: dict, history: list[dict], predicted: float | None = None) -> dict:
    prior = [r for r in history if r["query_id"] == record["query_id"]]
    current = fingerprint(record["sql"])
    recurrence = any(fingerprint(r["sql"]) == current for r in prior)
    opposition = (
        len(prior) >= 2
        and fingerprint(prior[-2]["sql"]) == current
        and fingerprint(prior[-1]["sql"]) != current
    )
    mismatch = not record["correct"] or (
        predicted is not None and predicted > 1 and record["speedup"] < 1
    )
    return {
        "recurrence": recurrence,
        "opposition": opposition,
        "mismatch": mismatch,
        "regression": record["correct"] and record["speedup"] < 0.95,
        "sql_sha256": current,
        "error": record.get("error"),
        "prior_observation_count": len(prior),
    }


def probes(record: dict) -> dict:
    tree = sqlglot.parse_one(record["sql"], read="duckdb")
    from sqlglot import exp

    return {
        "operator_probe": {
            "group_nodes": len(list(tree.find_all(exp.Group))),
            "window_nodes": len(list(tree.find_all(exp.Window))),
            "plan": record.get("plan"),
            "evidence_scope": "Parsed candidate and actual stored EXPLAIN, not estimated speed",
        },
        "contract_probe": {
            "correct": record["correct"],
            "error_category": record.get("error_category"),
            "error": record.get("error"),
            "schema": record.get("schema"),
            "result_sha256": record.get("result_sha256"),
        },
        "timing_probe": {
            "speedup": record["speedup"],
            "warm_seconds": record.get("warm_seconds"),
            "dispersion": record.get("dispersion"),
            "interpretation": "Repeated paired timings, not a causal attribution of operator cost",
        },
    }
