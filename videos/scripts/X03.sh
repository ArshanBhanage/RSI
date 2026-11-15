#!/usr/bin/env bash
set -euo pipefail
uv run queryforge doctor
sed -n '1,240p' src/queryforge/methods.py
uv run python -c 'import json; from pathlib import Path; xs=[json.load(open(p)) for p in Path("experiments/methods").glob("rsiflow-seed-*.json")]; assert len(xs)==2; print(json.dumps(xs,indent=2))'
