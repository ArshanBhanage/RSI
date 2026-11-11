"""Host-side container launcher and append-only measured evidence ledger."""

import fcntl
import json
import subprocess
import time
import uuid

from .dataset import MANIFEST, verify
from .provenance import ROOT, digest, identity, now, save

AUTHORITY = {
    "evaluate.py": ROOT / "sandbox/evaluate.py",
    "sql_safety.py": ROOT / "src/queryforge/sql_safety.py",
    "queries.json": ROOT / "experiments/workload/queries.json",
    "evaluation.json": ROOT / "configs/evaluation.json",
}
LOCK = ROOT / "configs/authority-lock.json"


def freeze() -> dict:
    image = subprocess.check_output(
        ["docker", "image", "inspect", "queryforge-eval:v1", "--format", "{{.Id}}"], text=True
    ).strip()
    value = {
        "files": {name: digest(path) for name, path in AUTHORITY.items()},
        "image": image,
        "budgets_sha256": digest(ROOT / "configs/budgets.json"),
    }
    if LOCK.exists() and json.loads(LOCK.read_text()) != value:
        raise ValueError("Authority already frozen; changes require a new experiment protocol")
    save(LOCK, value)
    return value


def evaluate(
    candidates: list[dict],
    method: str,
    generation: int = 0,
    seed: int = 17,
    final: bool = False,
    run_id: str | None = None,
) -> dict:
    verify()
    lock = json.loads(LOCK.read_text())
    for name, path in AUTHORITY.items():
        if digest(path) != lock["files"][name]:
            raise ValueError("Evaluator tampering detected: " + name)
    if digest(ROOT / "configs/budgets.json") != lock["budgets_sha256"]:
        raise ValueError("Budget changed after protocol freeze")
    dataset = json.loads(MANIFEST.read_text())
    role = "heldout" if final else "development"
    if not candidates or len(candidates) > 12:
        raise ValueError("Candidate batch budget violated")
    config = json.loads((ROOT / "configs/evaluation.json").read_text())
    request = {"seed": seed, "candidates": candidates, "final": final}
    name = "queryforge-" + uuid.uuid4().hex[:12]
    command = [
        "docker",
        "run",
        "--rm",
        "-i",
        "--name",
        name,
        "--network",
        "none",
        "--read-only",
        "--user",
        "65534:65534",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--pids-limit",
        "32",
        "--memory",
        "2g",
        "--cpus",
        "1",
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,size=64m",
    ]
    for filename, source in AUTHORITY.items():
        command += ["--mount", f"type=bind,src={source},dst=/authority/{filename},readonly"]
    for filename, key in [("trips.parquet", role), ("zones.csv", "zones")]:
        command += [
            "--mount",
            f"type=bind,src={ROOT / dataset[key]['path']},dst=/data/{filename},readonly",
        ]
    command += [lock["image"]]
    output = ROOT / "experiments/runs"
    output.mkdir(parents=True, exist_ok=True)
    # Serialize CPU benchmarks across all processes and hold the lock through ledger append.
    with (ROOT / ".local/benchmark.lock").open("w") as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        started = time.perf_counter()
        try:
            result = subprocess.run(
                command,
                input=json.dumps(request),
                text=True,
                capture_output=True,
                timeout=config["container_timeout_seconds"],
                check=False,
            )
            if result.returncode:
                raise RuntimeError(result.stderr[-4000:])
            actual = json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "rm", "-f", name], capture_output=True, check=False)
            actual = {
                "records": [
                    {
                        "query_id": c["query_id"],
                        "sql": c["sql"],
                        "correct": False,
                        "speedup": 0,
                        "error_category": "ContainerTimeout",
                    }
                    for c in candidates
                ]
            }
        record = {
            "id": uuid.uuid4().hex,
            "run_id": run_id,
            "utc": now(),
            "method": method,
            "generation": generation,
            "seed": seed,
            "final": final,
            "data_sha256": dataset[role]["sha256"],
            "evaluator_sha256": identity(lock),
            "wall_seconds": time.perf_counter() - started,
            **actual,
        }
        with (output / "evaluations.jsonl").open("a") as stream:
            stream.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def baseline() -> dict:
    queries = json.loads((ROOT / "experiments/workload/queries.json").read_text())
    result = evaluate(
        [{"query_id": q["id"], "sql": q["sql"]} for q in queries if q["partition"] != "heldout"],
        "fixed-baseline",
    )
    if not all(r["correct"] for r in result["records"]):
        raise ValueError("Baseline correctness failed; see evaluation ledger")
    save(ROOT / "experiments/manifests/baseline.json", result)
    return result
