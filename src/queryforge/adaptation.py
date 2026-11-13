"""Workflow research lessons with explicit boundaries from model-weight optimization."""

import json

from .provenance import ROOT


def workflow_comparison() -> dict:
    workflow = json.loads((ROOT / "experiments/labs/10.08.json").read_text())["result"]
    team = json.loads((ROOT / "experiments/labs/10.10.json").read_text())["result"]
    assert len(workflow["generations"]) == 2 and len(team["campaigns"]) == 2
    return {
        "comparison": {
            "RSIFlow": {
                "source": "https://arxiv.org/abs/2610.21791",
                "changed_object": "Diagnosed task component and reusable skill memory; released executable Meta is fixed.",
                "prefer_when": "A heterogeneous workflow has observable component bottlenecks and skills with measurable applicability.",
                "risk": "A task-specific successful intervention can become an unsupported universal memory entry.",
            },
            "Self-HPO": {
                "source": "https://arxiv.org/abs/2610.22791",
                "changed_object": "Alternating H-step harness search and P-step reinforcement learning of policy weights.",
                "prefer_when": "Training access and budget allow co-adapting weights and harness, with hard-task feedback between stages.",
                "risk": "Changing both components confounds gains unless each is separately frozen and evaluated.",
            },
        },
        "actual_evidence": {
            "workflow_revision": workflow["revision_proposal"],
            "workflow_generation_ids": [
                g["evaluation"]["id"] if g["evaluation"] else None for g in workflow["generations"]
            ],
            "conditional_memory_campaign_ids": [c["evaluation"]["id"] for c in team["campaigns"]],
            "inherited_workflow_hashes": [g["workflow_sha256"] for g in workflow["generations"]],
        },
        "interpretation": "Executable source/evidence audit of completed real trajectories. Existing flags and conditional memory illustrate routing and inheritance, not Self-HPO RL training or a faithful RSIFlow reproduction.",
    }


def adaptive_meta() -> dict:
    from .evaluator import evaluate
    from .proposals.codex_cli import propose
    from .provenance import identity, save
    from .search import proposals
    from .workflow import prepare

    history = json.loads((ROOT / "experiments/labs/10.08.json").read_text())["result"][
        "generations"
    ][-1]["evaluation"]["records"]
    schema = {
        "type": "object",
        "properties": {
            "route": {
                "type": "string",
                "enum": ["repair_contract", "simplify_aggregation", "rewrite_predicate"],
            },
            "diagnosis": {"type": "string"},
            "skill": {"type": "string"},
        },
        "required": ["route", "diagnosis", "skill"],
        "additionalProperties": False,
    }
    memory: list[dict] = []
    rounds = []
    for generation in [0, 1]:
        supported = [m for m in memory if m["accepted"]]
        meta = propose(
            "Diagnose actual SQL workflow bottlenecks and choose a component-specific intervention. Distill a conditional proposed skill, not a proven finding. "
            + json.dumps(
                {
                    "trace": [
                        {k: r.get(k) for k in ["query_id", "sql", "correct", "speedup", "error"]}
                        for r in history
                    ],
                    "supported_memory": supported,
                }
            ),
            schema,
            "bottleneck-meta",
        )
        routing = meta["response"]
        flags = {"preflight": True, "deduplicate": True, "instruction": routing["skill"]}
        candidate = proposals(
            ["q01", "q05"],
            2,
            "Workflow route: " + routing["route"] + ". " + routing["skill"],
            supported,
        )
        prepared = prepare(candidate["response"]["candidates"], flags)
        result = (
            evaluate(prepared["accepted"], "lab-10.13-adaptive-meta", generation=generation)
            if prepared["accepted"]
            else None
        )
        records = result["records"] if result else []
        accepted = (
            len(records) == 2
            and all(r["correct"] for r in records)
            and all(r["speedup"] >= 1.02 for r in records)
        )
        entry = {
            "generation": generation,
            "route": routing["route"],
            "skill": routing["skill"],
            "accepted": accepted,
            "scope": ["q01", "q05"],
            "evaluation_id": result["id"] if result else None,
        }
        memory.append(entry)
        rounds.append(
            {
                "generation": generation,
                "retrieved_memory": supported,
                "meta_proposal_id": meta["proposal_id"],
                "routing": routing,
                "candidate_proposal_id": candidate["proposal_id"],
                "preflight": prepared,
                "evaluation": result,
                "skill_entry": entry,
            }
        )
        history = records
    save(ROOT / "experiments/manifests/10.13-skills.json", memory)
    return {
        "meta_schema_sha256": identity(schema),
        "rounds": rounds,
        "memory": memory,
        "interpretation": "The executable controller is fixed. Real model diagnoses route interventions; skills enter supported memory only after both task speedups exceed 1.02 with correctness. Rejected skills remain visible and are not promoted. This small released-variant-inspired adaptation may show zero accepted skills.",
    }
