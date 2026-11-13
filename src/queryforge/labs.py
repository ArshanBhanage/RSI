"""Numbered research lessons grounded in persisted execution evidence."""

import json
import math

from .provenance import ROOT, digest, now, save


def ledger() -> list[dict]:
    path = ROOT / "experiments/runs/evaluations.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()]


def verify_claim(claim: dict, evaluation: dict) -> bool:
    records = evaluation.get("records", [])
    if not records or not all(r.get("correct") for r in records):
        return False
    measured = math.prod(r["baseline_median"] / r["candidate_median"] for r in records) ** (
        1 / len(records)
    )
    return (
        claim.get("evaluation_id") == evaluation["id"]
        and math.isclose(claim.get("speedup", 0), measured, rel_tol=1e-9)
        and bool(evaluation.get("data_sha256"))
        and bool(evaluation.get("evaluator_sha256"))
    )


def evidence_lab() -> dict:
    actual = json.loads((ROOT / "experiments/manifests/M03-fixed-improver.json").read_text())
    measured = actual["records"][0]["baseline_median"] / actual["records"][0]["candidate_median"]
    claim = {"evaluation_id": actual["id"], "speedup": measured}
    invalid = {"evaluation_id": "nonexistent-test-id", "speedup": 999}
    result = {
        "actual_claim": claim,
        "supported": verify_claim(claim, actual),
        "negative_contract_case": invalid,
        "negative_case_rejected": not verify_claim(invalid, actual),
        "interpretation": "One measured SQL rewrite is not proof of recursive improver improvement.",
    }
    assert result["supported"] and result["negative_case_rejected"]
    return result


RUNNERS = {"10.01": evidence_lab}


def run(lab_id: str) -> dict:
    if lab_id not in RUNNERS:
        raise ValueError("Lesson is not implemented: " + lab_id)
    report_path = ROOT / "experiments/labs" / f"{lab_id}.json"
    if report_path.exists():
        raise FileExistsError(
            "Verified evidence already exists; use a separate experiment checkout to rerun"
        )
    result = RUNNERS[lab_id]()
    report = {
        "lab_id": lab_id,
        "utc": now(),
        "video_status": "DEFERRED_BY_OWNER",
        "source_lock_sha256": digest(ROOT / "docs/references/source-lock.json"),
        "result": result,
    }
    save(ROOT / "experiments/labs" / f"{lab_id}.json", report)
    return report


def paper_audit() -> dict:
    audit = json.loads((ROOT / "research/paper-audit.json").read_text())
    sources = json.loads((ROOT / "docs/references/course-papers.json").read_text())
    source = next(p for p in sources if p["arxiv_id"] == audit["paper"])
    fields = [
        "citation",
        "changed_object",
        "heldout",
        "budget",
        "license",
        "cross_check",
        "adaptation",
    ]
    checks = {key: isinstance(audit.get(key), str) and len(audit[key]) > 20 for key in fields}
    checks["title_matches_publisher"] = (
        audit["citation"] in source["sources"][0]["metadata"]["citation_title"]
    )
    assert all(checks.values())
    return {
        "checks": checks,
        "audit": audit,
        "source_hashes": source["sources"],
        "interpretation": "Validator establishes audit completeness and title identity, not independent truth of paper claims.",
    }


RUNNERS["10.02"] = paper_audit


def budget_demo() -> dict:
    from .evaluator import evaluate
    from .search import proposals

    proposed = proposals(
        ["q01", "q02", "q03", "q04"],
        8,
        "Use two structurally different rewrites per task. This is initial calibration.",
    )
    actual = evaluate(proposed["response"]["candidates"], "lab-10.03-calibration")
    assert len(actual["records"]) == 8
    assert any(x["correct"] for x in actual["records"])
    return {
        "proposal_id": proposed["proposal_id"],
        "evaluation_id": actual["id"],
        "records": actual["records"],
        "interpretation": "Authentic calibration executions; no synthetic scorer labels and no recursive-improvement claim.",
    }


RUNNERS["10.03"] = budget_demo


def scoring_analysis() -> dict:
    from .search import fit, predict

    records = json.loads((ROOT / "experiments/labs/10.03.json").read_text())["result"]["records"]
    training = records[:4]
    validation = records[4:]
    model = fit(training)
    estimates = predict(model, validation)
    comparisons = [
        {
            "query_id": row["query_id"],
            "prediction": estimate,
            "measured_speedup": row["speedup"],
            "absolute_error": abs(estimate - row["speedup"]),
        }
        for row, estimate in zip(validation, estimates)
    ]
    assert all(math.isfinite(x["prediction"]) for x in comparisons)
    save(ROOT / "experiments/manifests/budget-scorer.json", model)
    return {
        "model": model,
        "training_evidence": "experiments/labs/10.03.json",
        "training_indices": list(range(4)),
        "validation_indices": list(range(4, 8)),
        "comparisons": comparisons,
        "mean_absolute_error": sum(x["absolute_error"] for x in comparisons) / len(comparisons),
        "interpretation": "Retrospective split analysis only. Four observations for nine features require regularization; this cannot establish prospective selection gains. Coefficients are frozen for the next lab.",
    }


RUNNERS["10.04"] = scoring_analysis


def prospective_selection() -> dict:
    """Freeze choices before revealing any transfer-task runtime labels."""
    import random

    from .evaluator import evaluate
    from .search import predict, proposals

    commitment_path = ROOT / "experiments/manifests/10.05-selection-commitment.json"
    if commitment_path.exists():
        raise RuntimeError("Existing prospective commitment must not be overwritten")
    model_path = ROOT / "experiments/manifests/budget-scorer.json"
    proposed = proposals(
        ["q05"],
        4,
        "Transfer evaluation: propose four distinct exact rewrites of the route aggregation. "
        "Explore predicate placement and aggregation layout. No runtime labels are available.",
    )
    candidates = proposed["response"]["candidates"]
    estimates = predict(json.loads(model_path.read_text()), candidates)
    scored = max(range(4), key=lambda i: estimates[i])
    random_choice = random.Random(17).randrange(4)
    commitment = {
        "utc": now(),
        "model_sha256": digest(model_path),
        "proposal_id": proposed["proposal_id"],
        "predictions": estimates,
        "scorer_choice": scored,
        "random_choice": random_choice,
        "operational_budget_per_arm": 1,
        "audit_protocol": "Evaluate all four after committing both choices; count every audit execution.",
    }
    save(commitment_path, commitment)
    measured = evaluate(candidates, "lab-10.05-prospective-transfer")
    assert len(measured["records"]) == 4
    return {
        "commitment": commitment,
        "evaluation_id": measured["id"],
        "records": measured["records"],
        "scorer_selected": measured["records"][scored],
        "random_selected": measured["records"][random_choice],
        "total_candidate_evaluations": 4,
        "interpretation": "One prospective transfer task with equal one-candidate selection budgets. All four candidates were measured for audit; no evaluation-cost saving or statistical superiority is claimed.",
    }


RUNNERS["10.05"] = prospective_selection


def diagnostic_demo() -> dict:
    from .diagnostics import inspect, probes
    from .evaluator import evaluate
    from .search import proposals

    transfer = json.loads((ROOT / "experiments/labs/10.05.json").read_text())["result"]
    history: list[dict] = []
    observations = []
    for record, prediction in zip(transfer["records"], transfer["commitment"]["predictions"]):
        observations.append(inspect(record, history, prediction))
        history.append(record)
    failed = transfer["records"][-1]
    diagnostic = probes(failed)
    naive = proposals(["q05"], 1, "Try a new rewrite. Previous candidate failed.")
    informed = proposals(
        ["q05"],
        1,
        "Use diagnostic inquiry before proposing: avoid the observed denied function and redundant aggregation. "
        "A SQL rewrite does not change the evaluator's allowed language.",
        [{"diagnostic": diagnostic, "anomalies": observations}],
    )
    actual = evaluate(
        naive["response"]["candidates"] + informed["response"]["candidates"],
        "lab-10.06-naive-vs-diagnostic",
    )
    return {
        "source_evaluation": transfer["evaluation_id"],
        "anomalies": observations,
        "probe": diagnostic,
        "arms": ["naive", "diagnostic"],
        "proposal_ids": [naive["proposal_id"], informed["proposal_id"]],
        "evaluation_id": actual["id"],
        "records": actual["records"],
        "interpretation": "One actual proposal and evaluator call per arm. Absence of recurrence or opposition is reported honestly. This diagnoses observed failures; no paper-level success-rate claim is made.",
    }


RUNNERS["10.06"] = diagnostic_demo


def diagnostic_probes() -> dict:
    from .diagnostics import probes
    from .evaluator import evaluate

    previous = json.loads((ROOT / "experiments/labs/10.06.json").read_text())["result"]
    transfer = json.loads((ROOT / "experiments/labs/10.05.json").read_text())["result"]
    repeat = evaluate(
        [{"query_id": r["query_id"], "sql": r["sql"]} for r in previous["records"]],
        "lab-10.07-repeat-probe",
    )
    counts = {
        kind: sum(bool(row[kind]) for row in previous["anomalies"])
        for kind in ["recurrence", "opposition", "mismatch", "regression"]
    }
    return {
        "counts": counts,
        "probes": [probes(row) for row in transfer["records"] + repeat["records"]],
        "evaluation_id": repeat["id"],
        "records": repeat["records"],
        "recommendations": {
            "recurrence": "No occurrence observed. If present, compare canonical SQL hashes before another evaluation.",
            "opposition": "No occurrence observed. If present, inspect the last two same-task transformations for conflicting constraints.",
            "mismatch": "ROW_NUMBER was rejected by the fixed language policy. Avoid that function; do not relax the evaluator. Predictions above one were not reliable guarantees.",
            "regression": "Inspect actual aggregation operators and repeated timing dispersion before proposing an early-filter rewrite. Operator cost causality remains unproven.",
        },
        "interpretation": "Schema/contract, operator and timing probes use actual executed artifacts. The fresh repeat checks persistence of the measured contrast; absent anomaly types are not manufactured.",
    }


RUNNERS["10.07"] = diagnostic_probes


def debugging_workflow() -> dict:
    from .evaluator import evaluate
    from .provenance import identity
    from .search import proposals
    from .workflow import INITIAL, prepare, revise

    previous = json.loads((ROOT / "experiments/labs/10.07.json").read_text())["result"]
    transfer = json.loads((ROOT / "experiments/labs/10.05.json").read_text())["result"]
    revision = revise({"recommendations": previous["recommendations"]}, INITIAL)
    policy = revision["response"]
    save(ROOT / "experiments/manifests/10.08-workflow.json", policy)
    control = prepare(transfer["records"], INITIAL)
    replay = prepare(transfer["records"], policy)
    runs = []
    for generation in [1, 2]:
        proposed = proposals(
            ["q05"],
            2,
            policy["instruction"],
            [{"prior_recommendations": previous["recommendations"]}],
        )
        filtered = prepare(proposed["response"]["candidates"], policy)
        measured = (
            evaluate(filtered["accepted"], "lab-10.08-inherited-workflow", generation=generation)
            if filtered["accepted"]
            else None
        )
        runs.append(
            {
                "generation": generation,
                "workflow_sha256": identity(policy),
                "proposal_id": proposed["proposal_id"],
                "preflight": filtered,
                "evaluation": measured,
            }
        )
    assert identity(policy) != identity(INITIAL)
    return {
        "parent": INITIAL,
        "descendant": policy,
        "parent_sha256": identity(INITIAL),
        "descendant_sha256": identity(policy),
        "revision_proposal": revision["proposal_id"],
        "control_replay": control,
        "descendant_replay": replay,
        "generations": runs,
        "interpretation": "Model-generated workflow flags alter actual preflight/deduplication execution and are inherited by two fresh generations. Replay is a structural safety check, not a new runtime experiment. No performance promotion or general recursive gain is claimed.",
    }


RUNNERS["10.08"] = debugging_workflow


from .scaling import comparison

RUNNERS["10.09"] = comparison

from .scaling import leader_followers

RUNNERS["10.10"] = leader_followers
