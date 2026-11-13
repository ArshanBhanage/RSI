"""Replay authentic recorded candidates to test monitor history boundaries."""

import json

from queryforge.diagnostics import inspect
from queryforge.provenance import ROOT


def test_current_event_is_not_its_own_recurrence():
    records = json.loads((ROOT / "experiments/labs/10.05.json").read_text())["result"]["records"]
    assert not inspect(records[0], [])["recurrence"]
    assert inspect(records[0], [records[0]])["recurrence"]
    assert inspect(records[0], [records[0], records[1]])["opposition"]
    assert not inspect(records[1], [records[0]])["opposition"]


def test_actual_policy_failure_is_mismatch():
    records = json.loads((ROOT / "experiments/labs/10.05.json").read_text())["result"]["records"]
    failed = next(r for r in records if not r["correct"])
    assert inspect(failed, [])["mismatch"]
