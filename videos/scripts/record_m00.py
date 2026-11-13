# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow==11.3.0", "pygments==2.19.2"]
# ///
"""Capture actual source and subprocess output, then compose a silent walkthrough."""

import hashlib
import json
import subprocess
import sys
import textwrap
import time
from datetime import UTC, datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / ".local/recording-M00"
WORK.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 23)
SMALL = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 19)
STYLE = get_style_by_name("monokai")
frames = []
events = []


def frame(title, body, note, seconds=9, python=False):
    path = WORK / f"{len(frames):04d}.png"
    canvas = Image.new("RGB", (1600, 1000), "#101720")
    draw = ImageDraw.Draw(canvas)
    draw.text((35, 25), "QueryForge-RSI | M00 | Source audit", font=FONT, fill="#79d9c4")
    draw.text((35, 75), title, font=FONT, fill="white")
    y = 130
    for line in body.splitlines():
        if python:
            x = 35
            for token, value in lex(line, PythonLexer()):
                value = value.rstrip("\n")
                color = STYLE.style_for_token(token)["color"] or "eeeeee"
                draw.text((x, y), value, font=SMALL, fill="#" + color)
                x += draw.textlength(value, font=SMALL)
        else:
            draw.text((35, y), line, font=SMALL, fill="#e1e7ef")
        y += 29
    for index, line in enumerate(textwrap.wrap(note, 112)):
        draw.text((35, 850 + index * 27), line, font=SMALL, fill="#ffd479")
    draw.text(
        (35, 955),
        "Silent annotated capture | actual files + executed output | reading pauses added",
        font=SMALL,
        fill="#9badbf",
    )
    canvas.save(path)
    frames.append((path, seconds))


frame(
    "Purpose and scope",
    "Lock the course before implementing its lessons.\n17 distinct lessons: 10.01 through 10.17.\nVerify immutable source bytes and inspect released method boundaries.\nThis is a source audit, not a SQL benchmark or RSI result.\nRecording includes real source code and a fresh network verification run.\nNo human or synthetic voice is present.",
    "Reproduce: python3 scripts/verify_sources.py. Source citations: docs/references/source-lock.md.",
)
source = ROOT / "scripts/verify_sources.py"
data = source.read_bytes()
events.append(
    {
        "kind": "source_capture",
        "path": str(source.relative_to(ROOT)),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
)
lines = data.decode().splitlines()
for start in range(0, len(lines), 23):
    frame(
        f"scripts/verify_sources.py | lines {start + 1}-{min(start + 23, len(lines))}",
        "\n".join(lines[start : start + 23]),
        "Read immutable bytes, compare SHA-256, validate ordered lesson IDs, and persist actual check outcomes.",
        python=True,
    )
lock = json.loads((ROOT / "docs/references/source-lock.json").read_text())
for start in [0, 9]:
    frame(
        "Pinned lesson mapping",
        "\n".join(f"{x['id']}  {x['title']}" for x in lock["labs"][start : start + 9]),
        "These names come from inspected upstream headings; they are not invented lesson titles.",
    )
command = [
    sys.executable,
    "scripts/verify_sources.py",
    "--output",
    "experiments/manifests/M00-recorded-sources.json",
]
started = time.monotonic()
result = subprocess.run(
    command,
    check=False,
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=180,
)
events.append(
    {
        "kind": "execution",
        "command": command,
        "utc": datetime.now(UTC).isoformat(),
        "elapsed_seconds": time.monotonic() - started,
        "returncode": result.returncode,
        "stdout": result.stdout,
    }
)
output = []
for line in result.stdout.splitlines():
    output.extend(textwrap.wrap(line, 125) or [""])
for start in range(0, len(output), 23):
    frame(
        "Fresh execution: python3 scripts/verify_sources.py",
        "\n".join(output[start : start + 23]),
        f"Actual exit code: {result.returncode}. Wall time: {events[-1]['elapsed_seconds']:.2f}s. Output is paginated with reading pauses.",
    )
frame(
    "Interpretation and next gate",
    "Source integrity passes only if every file and heading passes.\nDREAM-RSI: policy replay, promotion, then fresh rollout.\nAIDE2: original harness-evolution adaptation; official release not identified.\nRSIFlow release: skill evolution with a fixed executable Meta program.\nCourse RSI-Index equation conflicts with its worked example.\nSynthetic course demo outcomes are not QueryForge measurements.\nNext: M01 environment and authentication, after the M00 video gate.",
    "References and licenses: research/method-fidelity.md. No completed lab or method is claimed.",
)
trace = ROOT / "videos/M00-capture.json"
trace.write_text(json.dumps(events, indent=2) + "\n")
concat = WORK / "frames.txt"
concat.write_text(
    "".join(f"file '{p}'\nduration {duration}\n" for p, duration in frames)
    + f"file '{frames[-1][0]}'\n"
)
video = ROOT / "videos/renders/M00-source-audit.mp4"
video.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat),
        "-vf",
        "fps=25",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(video),
    ],
    check=True,
)
subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)
probe = json.loads(
    subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(video)]
    )
)
manifest = {
    "id": "M00",
    "path": str(video.relative_to(ROOT)),
    "sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
    "duration_seconds": float(probe["format"]["duration"]),
    "video_streams": sum(x["codec_type"] == "video" for x in probe["streams"]),
    "narration_mode": "silent_on_screen_explanation",
    "decode_verified": True,
    "source_sha256": hashlib.sha256(data).hexdigest(),
    "youtube_url": None,
    "status": "RECORDED_PENDING_UPLOAD",
    "command_returncode": result.returncode,
}
(ROOT / "videos/M00-video.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(manifest, indent=2))
sys.exit(result.returncode)
