"""Create a lesson's reproducibility page only after its actual report exists."""

import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
lab_id, explanation = sys.argv[1:3]
source = next(
    x
    for x in json.loads((root / "docs/references/source-lock.json").read_text())["labs"]
    if x["id"] == lab_id
)
report = root / "experiments/labs" / f"{lab_id}.json"
if not report.exists():
    raise SystemExit("Run the lesson before documenting completion")
folder = root / "codelabs" / lab_id.replace(".", "_")
folder.mkdir(parents=True, exist_ok=True)
(folder / "README.md").write_text(f"""# {lab_id} — {source["title"]}

{explanation}

Source: [pinned lesson](https://github.com/dlmastery/simple-coding-harness/blob/fabd4c79207df6a6a144c22fb1703fc074a048e7/{source["source_path"]}). This is an original QueryForge adaptation, not a reproduction of the source paper's benchmark results.

## Reproduce

Prerequisites: complete M00–M03 and all preceding labs; `uv sync --locked`, authenticated Codex CLI, running Docker and checksum-verified TLC data. From the repository root:

```sh
uv run queryforge lab run {lab_id}
```

Implementation: [shared lesson code](../../src/queryforge/labs.py), [protected evaluator](../../src/queryforge/evaluator.py), [protocol](../../docs/evaluation-protocol.md). Input contracts are checked by the runnable lesson; failures stop execution rather than manufacture success. The output is [the actual JSON report](../../experiments/labs/{lab_id}.json), which links the measurement or source evidence used. Read its interpretation together with the source-fidelity caveats. Missing source data, credentials or evidence is an error, not an offline simulation.

Video: deferred by owner until code verification and GitHub publication. No verified walkthrough link is claimed.
""")
p = root / "docs/milestones.md"
text = p.read_text()
text = text.replace(
    f"| L{lab_id} | NOT_STARTED | Prior milestone must pass. |",
    f"| L{lab_id} | CODE_VERIFIED | `experiments/labs/{lab_id}.json`; video deferred. |",
)
p.write_text(text)
