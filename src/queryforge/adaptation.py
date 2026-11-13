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
