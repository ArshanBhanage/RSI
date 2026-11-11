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
