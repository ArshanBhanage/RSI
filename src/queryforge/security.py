"""Live safety probes and source-grounded environment distinctions."""

import json
import subprocess
import sys

from .evaluator import evaluate
from .provenance import ROOT


def environment_lab() -> dict:
    output = ROOT / "experiments/manifests/10.16-security-boundaries.json"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/check_sandbox.py"), "--output", str(output)],
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    boundary = json.loads(output.read_text())
    payloads = [
        "SELECT * FROM read_parquet('../../etc/passwd')",
        "COPY trips TO '/tmp/leak.csv'",
        "INSTALL shellfs; LOAD shellfs; SELECT 1",
        "SELECT system('touch /tmp/queryforge-escape')",
    ]
    actual = evaluate(
        [{"query_id": "q01", "sql": sql} for sql in payloads], "security-adversarial-language"
    )
    assert boundary["passed"] and all(not r["correct"] for r in actual["records"])
    return {
        "boundary_checks": boundary,
        "language_checks": actual,
        "environments": {
            "RSIGym": {
                "source": "https://arxiv.org/abs/2610.10310",
                "mechanism": "Service-based training, inference, evaluation and sandboxes with shared budgets and permissions.",
                "fit": "Experiments spanning data, model and harness interventions.",
                "limit": "Service availability and budget accounting remain part of reproducibility.",
            },
            "Terminal-RSI": {
                "source": "https://arxiv.org/abs/2610.22192",
                "mechanism": "Alternating verified trajectory rewriting and critic-inheriting policy refinement, with turn-aware advantage estimation.",
                "fit": "Training terminal agents with verifier and partial-progress signals.",
                "limit": "Not merely a terminal sandbox; requires model/critic training infrastructure not reproduced here.",
            },
            "R2Orch": {
                "source": "https://arxiv.org/abs/2610.22740",
                "mechanism": "Inner orchestration self-play and outer skill withdrawal/internalization guided by recursive learnability.",
                "fit": "Training task selection and orchestration when repeated controlled rollouts are available.",
                "limit": "A single task score does not establish recursive learnability or successful skill internalization.",
            },
        },
        "interpretation": "Actual SQL and Docker negative tests exercise this project’s boundary. QueryForge is a local protected SQL environment, not any of these training platforms. Denied attack inputs are contract tests, not fabricated taxi data or optimization gains.",
    }
