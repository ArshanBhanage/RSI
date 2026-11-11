"""Non-secret environment checks; installed tools alone do not establish readiness."""

import importlib.metadata
import platform
import shutil
import subprocess
import sys

from .provenance import ROOT, now, save


def check() -> dict:
    checks = {}
    for name, command in {
        "uv": ["uv", "--version"],
        "docker": ["docker", "info", "--format", "{{.ServerVersion}}"],
        "codex": ["codex", "login", "status"],
        "github": ["gh", "api", "user", "--jq", ".login"],
        "ffmpeg": ["ffmpeg", "-version"],
    }.items():
        if not shutil.which(command[0]):
            checks[name] = {"ok": False, "detail": "not on PATH"}
            continue
        try:
            result = subprocess.run(
                command, check=False, capture_output=True, text=True, timeout=30
            )
            text = (result.stdout + result.stderr).splitlines()
            checks[name] = {"ok": result.returncode == 0, "detail": text[0] if text else ""}
        except subprocess.TimeoutExpired:
            checks[name] = {"ok": False, "detail": "timeout"}
    env = ROOT / ".env"
    checks["local_env"] = {"ok": env.exists() and env.stat().st_mode & 0o077 == 0}
    report = {
        "utc": now(),
        "python": sys.version,
        "platform": platform.platform(),
        "dependencies": {
            x: importlib.metadata.version(x)
            for x in ["duckdb", "pyarrow", "sqlglot", "numpy", "typer", "pydantic"]
        },
        "checks": checks,
        "passed": all(x["ok"] for x in checks.values()),
    }
    save(ROOT / "experiments/manifests/environment.json", report)
    return report
