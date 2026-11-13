"""The workflow guard uses authentic failures and never changes evaluation authority."""

import json

from queryforge.provenance import ROOT
from queryforge.workflow import INITIAL, prepare


def test_guard_rejects_observed_invalid_candidate_and_duplicates():
    records = json.loads((ROOT / "experiments/labs/10.05.json").read_text())["result"]["records"]
    policy = {**INITIAL, "preflight": True, "deduplicate": True}
    control = prepare(records, INITIAL)
    guarded = prepare(records + [records[0]], policy)
    assert len(control["accepted"]) == len(records)
    assert len(guarded["rejected"]) == 2
    assert any("ROW_NUMBER" in r["preflight_error"] for r in guarded["rejected"])
    assert any("Repeated" in r["preflight_error"] for r in guarded["rejected"])
