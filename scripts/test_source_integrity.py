"""Exercise offline integrity boundaries using the authentic locked course map."""

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile

import verify_sources

root = Path(__file__).resolve().parents[1]
lock = json.loads((root / 'docs/references/source-lock.json').read_text())
entry = lock['files'][0]
content = (root / '.local/sources' / entry['sha256']).read_bytes()
checks = []
with tempfile.TemporaryDirectory() as directory:
    verify_sources.ROOT = Path(directory)
    cache = verify_sources.ROOT / '.local/sources' / entry['sha256']
    cache.parent.mkdir(parents=True)
    checks.append({'check': 'missing_cache_fails_closed',
                   'passed': not verify_sources.check_file(entry, True)['ok']})
    cache.write_bytes(content)
    checks.append({'check': 'authentic_cached_source_passes',
                   'passed': verify_sources.check_file(entry, True)['ok']})
    cache.write_bytes(content + b'\n')
    checks.append({'check': 'altered_source_rejected',
                   'passed': not verify_sources.check_file(entry, True)['ok']})
result = {'utc': datetime.now(timezone.utc).isoformat(),
          'scope': 'source integrity contract tests; no domain data or mocked services',
          'checks': checks, 'passed': all(check['passed'] for check in checks)}
(root / 'experiments/manifests/M00-contract-checks.json').write_text(
    json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['passed'] else 1)
