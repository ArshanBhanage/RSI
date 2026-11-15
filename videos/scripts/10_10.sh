#!/usr/bin/env bash
set -euo pipefail
uv run queryforge doctor
sed -n '1,240p' src/queryforge/labs.py
uv run python -c 'import json; x=json.load(open("experiments/labs/10.10.json")); assert x["lab_id"]=="10.10"; print(json.dumps(x,indent=2))'
