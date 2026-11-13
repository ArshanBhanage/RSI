"""Execute negative SQL and actual container-boundary checks; never report as gains."""

import argparse
import json
import subprocess
from pathlib import Path

from queryforge.evaluator import AUTHORITY, LOCK, evaluate
from queryforge.provenance import ROOT, now, save

parser = argparse.ArgumentParser()
parser.add_argument("--output", default=str(ROOT / "experiments/manifests/M03-security.json"))
args = parser.parse_args()

negative = [
    {"query_id": "q01", "sql": "SELECT 1 AS hour, 1 AS trips"},
    {"query_id": "q01", "sql": "SELECT * FROM read_csv('/etc/passwd')"},
    {"query_id": "q07", "sql": "SELECT COUNT(*) FROM trips"},
    {
        "query_id": "q01",
        "sql": "SELECT SUM(a.trip_distance * b.trip_distance) FROM trips a CROSS JOIN trips b",
    },
]
record = evaluate(negative, "security-negative-tests")
checks = [
    {"name": "semantic_mismatch", "passed": not record["records"][0]["correct"]},
    {"name": "external_file_denied", "passed": not record["records"][1]["correct"]},
    {"name": "heldout_query_denied", "passed": not record["records"][2]["correct"]},
    {
        "name": "query_interrupted",
        "passed": record["records"][3].get("error_category") == "InterruptException",
    },
]
lock = json.loads(LOCK.read_text())
code = """
import os,socket,json
result={'nonroot':os.getuid()==65534}
try:
 open('/authority/evaluation.json','w').write('tamper')
 result['readonly']=False
except OSError: result['readonly']=True
try:
 socket.create_connection(('1.1.1.1',443),timeout=2)
 result['network_denied']=False
except OSError: result['network_denied']=True
print(json.dumps(result))
"""
command = [
    "docker",
    "run",
    "--rm",
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
    "--mount",
    f"type=bind,src={AUTHORITY['evaluation.json']},dst=/authority/evaluation.json,readonly",
    "--entrypoint",
    "python",
    lock["image"],
    "-c",
    code,
]
actual = json.loads(subprocess.check_output(command, text=True, timeout=30))
checks += [{"name": k, "passed": v} for k, v in actual.items()]
save(
    Path(args.output),
    {
        "utc": now(),
        "checks": checks,
        "evaluation_id": record["id"],
        "passed": all(x["passed"] for x in checks),
    },
)
print(json.dumps(checks, indent=2))
raise SystemExit(0 if all(x["passed"] for x in checks) else 1)
