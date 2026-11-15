#!/usr/bin/env bash
set -euo pipefail
uv run queryforge doctor
sed -n '1,240p' src/queryforge/labs.py
uv run python -c 'import json; x=json.load(open("experiments/labs/10.12.json")); assert x["lab_id"]=="10.12"; print(json.dumps(x,indent=2))'
