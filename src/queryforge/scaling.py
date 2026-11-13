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


def leader_followers() -> dict:
    from concurrent.futures import ThreadPoolExecutor

    from .proposals.codex_cli import propose
    from .search import proposals

    schema = {
        "type": "object",
        "properties": {
            "hour_orientation": {"type": "string"},
            "route_orientation": {"type": "string"},
        },
        "required": ["hour_orientation", "route_orientation"],
        "additionalProperties": False,
    }
    leader = propose(
        "Lead two SQL researchers. Assign complementary concrete orientations: one optimizes hourly COUNT grouping, the other first-week pickup/dropoff route COUNT grouping. Preserve exact semantics, NULLs, anomalous dates and types. Workers use fixed external validation. Do not claim results.",
        schema,
        "leader-orientations",
    )
    roles = [
        ("q01", leader["response"]["hour_orientation"]),
        ("q05", leader["response"]["route_orientation"]),
    ]
    memory: list[dict] = []
    campaigns = []
    for campaign in [0, 1]:
        inputs = [
            {
                "query_id": qid,
                "orientation": orientation,
                "findings": [m for m in memory if m["query_id"] == qid and m["resolved"]],
            }
            for qid, orientation in roles
        ]

        def worker(task):
            return proposals([task["query_id"]], 1, task["orientation"], task["findings"])

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(worker, inputs))
        measured = evaluate(
            [r["response"]["candidates"][0] for r in results],
            "lab-10.10-leader-followers",
            generation=campaign,
        )
        for index, row in enumerate(measured["records"]):
            memory.append(
                {
                    "query_id": row["query_id"],
                    "resolved": row["correct"],
                    "claim_scope": "semantic correctness only; performance remains measured task-specific evidence",
                    "sql": row["sql"],
                    "speedup": row["speedup"],
                    "evaluation_id": measured["id"],
                    "record_index": index,
                    "error": row.get("error"),
                }
            )
        campaigns.append(
            {
                "campaign": campaign,
                "worker_inputs": inputs,
                "proposal_ids": [r["proposal_id"] for r in results],
                "evaluation": measured,
            }
        )
    return {
        "leader_proposal_id": leader["proposal_id"],
        "roles": roles,
        "campaigns": campaigns,
        "memory": memory,
        "interpretation": "One real leader model call and two bounded real researcher calls per campaign. Only task-matching correctness-supported findings are shared in campaign two. CPU evaluations are serialized. This is a small coordination adaptation, not a reproduction of large persistent research teams.",
    }


def swarm_evolution() -> dict:
    from concurrent.futures import ThreadPoolExecutor

    from .search import proposals

    orientations = [
        "Explore early filtering before grouping.",
        "Explore an exact staged aggregation with correct BIGINT output.",
        "Explore a minimal CTE layout and justify its hypothesis.",
        "Explore aggregation expression simplification.",
        "Explore a different exact predicate representation without dropping anomalous dates.",
    ]

    def worker(instruction):
        return proposals(["q05"], 1, instruction)

    with ThreadPoolExecutor(max_workers=5) as pool:
        initial = list(pool.map(worker, orientations))
    population = evaluate(
        [p["response"]["candidates"][0] for p in initial], "lab-10.11-swarm-population"
    )
    ranked = sorted(
        enumerate(population["records"]),
        key=lambda pair: pair[1]["speedup"] if pair[1]["correct"] else 0,
        reverse=True,
    )
    parents = ranked[:2]
    feedback = [
        {
            "index": i,
            "sql": r["sql"],
            "correct": r["correct"],
            "speedup": r["speedup"],
            "error": r.get("error"),
        }
        for i, r in parents
    ]
    mutation = proposals(
        ["q05"],
        1,
        "Mutate the first parent hypothesis and SQL based on its measured feedback. Describe the changed component.",
        feedback[:1],
    )
    recombination = proposals(
        ["q05"],
        1,
        "Recombine compatible predicate/aggregation components from both parents. State which component comes from which parent; if no useful complement exists, state that limitation instead of inventing it.",
        feedback,
    )
    descendants = evaluate(
        mutation["response"]["candidates"] + recombination["response"]["candidates"],
        "lab-10.11-swarm-descendants",
        generation=1,
    )
    return {
        "orientations": orientations,
        "initial_proposal_ids": [p["proposal_id"] for p in initial],
        "population": population,
        "selected_parents": feedback,
        "descendant_proposal_ids": [mutation["proposal_id"], recombination["proposal_id"]],
        "operators": ["feedback_guided_mutation", "component_recombination"],
        "descendants": descendants,
        "interpretation": "Five actual researcher subprocesses and two subsequent model-generated descendants, all externally evaluated. Parent evidence and component rationales are retained. SQL population evolution alone is not proof that the improver recursively improved.",
    }
