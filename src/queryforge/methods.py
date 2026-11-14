"""Bounded method adaptations with genuine inherited improver state."""

import json
import math
import uuid
from typing import Any

from .evaluator import evaluate
from .proposals.codex_cli import propose
from .provenance import ROOT, identity, now, save
from .search import proposals

METHODS = {"dream-rsi", "aide2", "rsiflow", "fixed"}


def _score(records: list[dict]) -> dict:
    by_task = {}
    for query_id in ["q01", "q05"]:
        rows = [row for row in records if row["query_id"] == query_id and row["correct"]]
        by_task[query_id] = max((row["speedup"] for row in rows), default=0)
    return {"by_task": by_task, "geomean": math.sqrt(by_task["q01"] * by_task["q05"])}


def _revise(method: str, state: dict, trace: list[dict]) -> dict:
    schema = {
        "type": "object",
        "properties": {
            "instruction": {"type": "string"},
            "preflight": {"type": "boolean"},
            "deduplicate": {"type": "boolean"},
            "diagnosis": {"type": "string"},
        },
        "required": ["instruction", "preflight", "deduplicate", "diagnosis"],
        "additionalProperties": False,
    }
    mechanisms = {
        "dream-rsi": "Replay the accumulated discovery tree offline and rewrite the exploration policy for a later fresh online generation.",
        "aide2": "Propose a descendant research harness; external selection stays fixed and the accepted descendant is inherited.",
        "rsiflow": "Diagnose the bottleneck, choose a component workflow, and distill only conditional evidence into improvement memory.",
    }
    return propose(
        mechanisms[method]
        + " Preserve exact SQL semantics and the external evaluator. Return executable routing flags and an instruction, without performance claims. "
        + json.dumps({"parent": state, "observed_trace": trace}),
        schema,
        method + "-improver-revision",
    )


def run(method: str, seed: int) -> dict:
    if method not in METHODS:
        raise ValueError("Unknown method")
    destination = ROOT / "experiments/methods" / f"{method}-seed-{seed}.json"
    if destination.exists():
        return json.loads(destination.read_text())
    run_id = uuid.uuid4().hex
    state: dict[str, Any] = {
        "instruction": "Explore two structurally distinct exact SQL rewrites per task.",
        "preflight": False,
        "deduplicate": False,
        "version": 0,
    }
    lineage = []
    accumulated: list[dict] = []
    stable_state = state
    pending_revision: dict | None = None
    for generation in range(3):
        batch = proposals(["q01", "q05"], 4, state["instruction"], accumulated[-8:])
        measured = evaluate(
            batch["response"]["candidates"], method, generation=generation, seed=seed, run_id=run_id
        )
        score = _score(measured["records"])
        node = {
            "generation": generation,
            "state": state,
            "state_sha256": identity(state),
            "proposal_id": batch["proposal_id"],
            "evaluation": measured,
            "score": score,
        }
        if pending_revision is not None:
            accepted = all(value >= 1.02 for value in score["by_task"].values())
            node["tested_revision_proposal_id"] = pending_revision["proposal_id"]
            node["accepted"] = accepted
            node["acceptance_rule"] = "correct best candidate speedup >= 1.02 on both q01 and q05"
            if accepted:
                stable_state = state
            else:
                state = stable_state
            pending_revision = None
        accumulated.extend(
            {
                "generation": generation,
                "query_id": row["query_id"],
                "correct": row["correct"],
                "speedup": row["speedup"],
                "error": row.get("error"),
            }
            for row in measured["records"]
        )
        if method != "fixed" and generation < 2:
            revision = _revise(method, state, accumulated)
            candidate_state = {**revision["response"], "version": state["version"] + 1}
            node["revision_proposal_id"] = revision["proposal_id"]
            node["candidate_state"] = candidate_state
            stable_state = state
            state = candidate_state
            pending_revision = revision
        lineage.append(node)
    final_batch = proposals(
        ["q07", "q08"],
        2,
        state["instruction"] + " This is the single final transfer proposal.",
        accumulated[-8:],
    )
    final = evaluate(
        final_batch["response"]["candidates"],
        method,
        generation=3,
        seed=seed,
        final=True,
        run_id=run_id,
    )
    report = {
        "method": method,
        "seed": seed,
        "run_id": run_id,
        "utc": now(),
        "budget": json.loads((ROOT / "configs/budgets.json").read_text()),
        "lineage": lineage,
        "frozen_state": state,
        "frozen_state_sha256": identity(state),
        "final_proposal_id": final_batch["proposal_id"],
        "heldout_evaluation": final,
        "accepted_generations": sum(bool(node.get("accepted")) for node in lineage),
        "fidelity": {
            "dream-rsi": "Policy replay/rewrite adaptation; not the paper benchmark or exact replay fitness.",
            "aide2": "Original harness-evolution adaptation; no official complete implementation was identified.",
            "rsiflow": "Released skill/workflow-variant adaptation; executable Meta remains fixed.",
            "fixed": "Non-evolving matched evaluator-call baseline.",
        }[method],
    }
    save(destination, report)
    return report


def run_all(method: str) -> list[dict]:
    budgets = json.loads((ROOT / "configs/budgets.json").read_text())
    return [run(method, seed) for seed in budgets["seeds"]]


def compare(verify: bool = True) -> dict:
    budgets = json.loads((ROOT / "configs/budgets.json").read_text())
    methods = ["fixed", "dream-rsi", "aide2", "rsiflow"]
    reports = {
        method: [
            json.loads((ROOT / "experiments/methods" / f"{method}-seed-{seed}.json").read_text())
            for seed in budgets["seeds"]
        ]
        for method in methods
    }
    rows = []
    for method, runs in reports.items():
        for report in runs:
            search_records = [record for node in report["lineage"] for record in node["evaluation"]["records"]]
            final_records = report["heldout_evaluation"]["records"]
            rows.append({
                "method": method, "seed": report["seed"],
                "search_candidates": len(search_records),
                "search_correct": sum(row["correct"] for row in search_records),
                "accepted_generations": report["accepted_generations"],
                "heldout_correct": sum(row["correct"] for row in final_records),
                "heldout_speedups": [row["speedup"] for row in final_records],
                "heldout_geomean": math.prod(row["speedup"] if row["correct"] else 0 for row in final_records) ** (1 / len(final_records)),
                "run_id": report["run_id"], "frozen_state_sha256": report["frozen_state_sha256"],
            })
    if verify:
        assert all(row["search_candidates"] == budgets["generations"] * budgets["candidates_per_generation"] for row in rows)
        assert {row["seed"] for row in rows} == set(budgets["seeds"])
        assert {row["method"] for row in rows} == set(methods)
    result = {
        "verified": verify, "budget_sha256": identity(budgets), "rows": rows,
        "interpretation": "Matched 12-candidate search budgets and a single two-task held-out transfer evaluation per seed. Meta-call costs differ and are visible in proposal records. Small samples and shared model/provider limit inference; zero gains and regressions are retained.",
    }
    save(ROOT / "experiments/reports/comparison.json", result)
    return result
