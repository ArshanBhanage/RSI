"""Executable preflight and deduplication policy, independent of the protected authority."""

from .diagnostics import fingerprint
from .proposals.codex_cli import propose
from .sql_safety import validate

INITIAL = {"preflight": False, "deduplicate": False, "instruction": "Explore exact SQL rewrites."}


def revise(feedback: dict, parent: dict) -> dict:
    import json

    schema = {
        "type": "object",
        "properties": {
            "preflight": {"type": "boolean"},
            "deduplicate": {"type": "boolean"},
            "instruction": {"type": "string"},
        },
        "required": ["preflight", "deduplicate", "instruction"],
        "additionalProperties": False,
    }
    return propose(
        "Revise the executable proposal workflow based on observed failures. "
        "preflight runs the public SQL language contract before expensive benchmarking; "
        "deduplicate rejects repeated canonical same-task SQL. Neither changes external scoring. "
        "The instruction guides future proposals. Return a concrete useful descendant. "
        + json.dumps({"parent": parent, "feedback": feedback}),
        schema,
        "diagnostic-workflow-revision",
    )


def prepare(candidates: list[dict], policy: dict, history: list[dict] | None = None) -> dict:
    seen = {(r["query_id"], fingerprint(r["sql"])) for r in history or []}
    accepted, rejected = [], []
    for candidate in candidates:
        key = (candidate["query_id"], fingerprint(candidate["sql"]))
        try:
            if policy["preflight"]:
                validate(candidate["sql"])
            if policy["deduplicate"] and key in seen:
                raise ValueError("Repeated same-task canonical SQL")
        except ValueError as error:
            rejected.append({**candidate, "preflight_error": str(error)})
        else:
            accepted.append(candidate)
        seen.add(key)
    return {"accepted": accepted, "rejected": rejected}
