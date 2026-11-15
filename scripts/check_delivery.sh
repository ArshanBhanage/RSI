#!/usr/bin/env bash
set -euo pipefail
test "$(find codelabs -mindepth 2 -maxdepth 2 -name README.md | wc -l | tr -d ' ')" = 17
test "$(find experiments/labs -maxdepth 1 -name '10.*.json' | wc -l | tr -d ' ')" = 17
for method in dream-rsi aide2 rsiflow; do
  test "$(find experiments/methods -maxdepth 1 -name "$method-seed-*.json" | wc -l | tr -d ' ')" = 2
done
test -f experiments/reports/comparison.json
test -f site/index.html
for id in $(seq -w 1 17); do test -f "site/labs/10.$id/index.html"; done
for method in dream-rsi aide2 rsiflow; do test -f "site/methods/$method/index.html"; done
test "$(git ls-files '.env' 'data/raw/*' '.local/*' 'videos/renders/*' | wc -l | tr -d ' ')" = 0
if git grep -nE '(ghp_|sk-[A-Za-z0-9]{20,}|BEGIN (RSA|OPENSSH) PRIVATE KEY)' -- . ':!uv.lock' ':!scripts/check_delivery.sh'; then
  echo 'Potential secret detected' >&2
  exit 1
fi
uv run python - <<'PY'
import json
from pathlib import Path
manifest=json.loads(Path('videos/VIDEO_MANIFEST.json').read_text())
assert len(manifest)==20
assert all(not row.get('youtube_verified',False) for row in manifest)
comparison=json.loads(Path('experiments/reports/comparison.json').read_text())
assert comparison['verified'] and len(comparison['rows'])==8
print('delivery structure verified; videos honestly pending owner upload')
PY
