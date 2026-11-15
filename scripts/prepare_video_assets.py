"""Create honest recording commands and planned narration; never mark a video recorded."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
items = [
    (f"10.{number:02d}", f"Section 10.{number:02d} evidence walkthrough") for number in range(1, 18)
] + [
    ("X01", "DREAM-RSI replay policy deep dive"),
    ("X02", "AIDE²-inspired harness lineage"),
    ("X03", "RSIFlow bottleneck and skill memory"),
]
method = {"X01": "dream-rsi", "X02": "aide2", "X03": "rsiflow"}
(ROOT / "videos/scripts").mkdir(parents=True, exist_ok=True)
(ROOT / "videos/transcripts").mkdir(parents=True, exist_ok=True)
manifest = []
for video_id, title in items:
    stem = video_id.replace(".", "_")
    if video_id.startswith("10."):
        report = f"experiments/labs/{video_id}.json"
        repo_path = f"codelabs/{stem}/"
        verify = f'uv run python -c \'import json; x=json.load(open("{report}")); assert x["lab_id"]=="{video_id}"; print(json.dumps(x,indent=2))\''
        code = "src/queryforge/labs.py"
    else:
        slug = method[video_id]
        report = f"experiments/methods/{slug}-seed-17.json"
        repo_path = f"research/methods/{'dream_rsi' if slug == 'dream-rsi' else slug}/"
        verify = f'uv run python -c \'import json; from pathlib import Path; xs=[json.load(open(p)) for p in Path("experiments/methods").glob("{slug}-seed-*.json")]; assert len(xs)==2; print(json.dumps(xs,indent=2))\''
        code = "src/queryforge/methods.py"
    script = ROOT / "videos/scripts" / f"{stem}.sh"
    script.write_text(
        f"#!/usr/bin/env bash\nset -euo pipefail\nuv run queryforge doctor\nsed -n '1,240p' {code}\n{verify}\n"
    )
    script.chmod(0o755)
    narration = ROOT / "videos/transcripts" / f"{stem}-planned.md"
    narration.write_text(
        f"# {video_id} — {title}\n\nStatus: planned owner narration; this is not a transcript of recorded speech.\n\n"
        "- 00:00 Identify the lesson, pinned source and changed object.\n"
        "- 00:20 Walk through the actual implementation and fixed authority boundary.\n"
        "- 01:20 Run the recording script and show its contemporaneous evidence verification.\n"
        "- 02:15 Explain correctness, latency, cost, failure and whether recursive improvement occurred.\n"
        "- 03:00 Show the reproduction command, source citation and fidelity limitation.\n"
    )
    manifest.append(
        {
            "lab_id": video_id,
            "title": title,
            "repo_path": repo_path,
            "recording_script": str(script.relative_to(ROOT)),
            "local_video_path": None,
            "local_sha256": None,
            "duration_seconds": None,
            "narration_mode": "NEEDS_OWNER_NARRATION",
            "transcript_path": str(narration.relative_to(ROOT)),
            "youtube_url": None,
            "youtube_verified": False,
            "source_commit": None,
            "run_manifest": report,
            "status": "PENDING_OWNER_RECORDING_AND_UPLOAD",
        }
    )
(ROOT / "videos/VIDEO_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"entries": len(manifest), "recorded": 0, "youtube_verified": 0}))
