"""Re-fetch immutable source files and fail closed on changed bytes or lab IDs."""

import argparse
import concurrent.futures
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def check_file(entry, offline):
    cache = ROOT / ".local/sources" / entry["sha256"]
    try:
        if offline:
            content = cache.read_bytes()
        else:
            with urlopen(entry["url"], timeout=45) as response:
                content = response.read()
        actual = hashlib.sha256(content).hexdigest()
        if actual != entry["sha256"]:
            raise ValueError("SHA-256 mismatch")
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(content)
        return {
            "path": entry["path"],
            "repository": entry["repository"],
            "sha256": actual,
            "ok": True,
        }
    except (OSError, ValueError) as error:
        return {
            "path": entry["path"],
            "repository": entry["repository"],
            "ok": False,
            "error": str(error),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument(
        "--output", type=Path, default=ROOT / "experiments/manifests/M00-sources.json"
    )
    args = parser.parse_args()
    raw = (ROOT / "docs/references/source-lock.json").read_bytes()
    lock = json.loads(raw)
    expected = [f"10.{number:02d}" for number in range(1, 18)]
    if [lab["id"] for lab in lock["labs"]] != expected:
        raise ValueError("Expected exactly 17 distinct, ordered course labs")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        checks = list(pool.map(lambda item: check_file(item, args.offline), lock["files"]))
    for lab in lock["labs"]:
        entry = next(item for item in lock["files"] if item["path"] == lab["source_path"])
        cache = ROOT / ".local/sources" / entry["sha256"]
        content = cache.read_text() if cache.exists() else ""
        checks.append(
            {
                "path": lab["source_path"],
                "check": "lesson_heading",
                "ok": bool(re.search(r"^# " + re.escape(lab["id"]) + r" · ", content)),
            }
        )
    result = {
        "schema_version": 1,
        "milestone": "M00",
        "scope": "source integrity only; not a passed milestone or experiment",
        "utc": datetime.now(UTC).isoformat(),
        "offline": args.offline,
        "lock_sha256": hashlib.sha256(raw).hexdigest(),
        "lab_count": len(lock["labs"]),
        "checks": checks,
        "passed": all(check["ok"] for check in checks),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for check in checks:
        print(("PASS " if check["ok"] else "FAIL ") + check["path"])
    print(json.dumps({key: result[key] for key in ["milestone", "lab_count", "passed", "scope"]}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
