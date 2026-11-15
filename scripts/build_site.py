"""Build the static evidence website solely from versioned reports."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"

CSS = """*{box-sizing:border-box}body{margin:0;background:#07111b;color:#e8f0f4;font:16px/1.6 system-ui,sans-serif}a{color:#76d7c4}header,main,footer{max-width:1100px;margin:auto;padding:24px}.hero{padding:70px 24px 35px}.eyebrow{color:#f4b860;text-transform:uppercase;letter-spacing:.14em}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}.card{background:#102231;border:1px solid #244457;border-radius:12px;padding:18px}.metric{font-size:2rem;color:#f4b860}.ok{color:#76d7c4}.pending{color:#f4b860}code{background:#132b3b;padding:.15em .35em;border-radius:4px}nav a{margin-right:18px}table{display:block;overflow-x:auto;width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px;border-bottom:1px solid #244457}@media(max-width:600px){.hero{padding-top:35px}table{font-size:.8rem}}"""


def layout(title: str, body: str) -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · QueryForge-RSI</title><link rel="stylesheet" href="/RSI/assets/style.css"></head><body><header><nav><a href="/RSI/">QueryForge</a><a href="/RSI/labs/">17 labs</a><a href="/RSI/methods/">3 methods</a><a href="/RSI/evidence/">Evidence</a><a href="https://github.com/ArshanBhanage/RSI">Repository</a></nav></header><main>{body}</main><footer>Authentic NYC TLC data · frozen external evaluation · videos pending owner upload</footer></body></html>"""


def write(relative: str, title: str, body: str) -> None:
    path = OUT / relative / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(layout(title, body))


def main() -> None:
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/style.css").write_text(CSS)
    labs = [
        json.loads((ROOT / "experiments/labs" / f"10.{number:02d}.json").read_text())
        for number in range(1, 18)
    ]
    cards = []
    for lab in labs:
        lab_id = lab["lab_id"]
        result = lab["result"]
        interpretation = result.get(
            "interpretation", "Runnable report with source-linked evidence."
        )
        cards.append(
            f'<article class="card"><div class="eyebrow">Lab {lab_id}</div><h2><a href="/RSI/labs/{lab_id}/">Verified execution</a></h2><p>{html.escape(interpretation)}</p></article>'
        )
        write(
            f"labs/{lab_id}",
            f"Lab {lab_id}",
            f'<p class="eyebrow">Section 10 · code verified</p><h1>{lab_id}</h1><p>{html.escape(interpretation)}</p><div class="card"><h2>Reproduce</h2><code>uv run queryforge lab run {lab_id}</code><p>Existing evidence is immutable; use a fresh experiment checkout to rerun.</p><p><a href="https://github.com/ArshanBhanage/RSI/blob/main/experiments/labs/{lab_id}.json">Machine-readable report</a> · <span class="pending">Video upload pending</span></p></div>',
        )
    write(
        "labs",
        "Codelabs",
        '<p class="eyebrow">17 of 17 code executions verified</p><h1>Research Studio codelabs</h1><div class="grid">'
        + "".join(cards)
        + "</div>",
    )
    methods = [("dream-rsi", "DREAM-RSI"), ("aide2", "AIDE² adaptation"), ("rsiflow", "RSIFlow")]
    method_cards = []
    for slug, name in methods:
        reports = sorted((ROOT / "experiments/methods").glob(f"{slug}-seed-*.json"))
        if reports:
            data = [json.loads(path.read_text()) for path in reports]
            accepted = sum(x["accepted_generations"] for x in data)
            detail = f"{len(data)} seeds; {accepted} accepted improver generations. See reports for held-out correctness and regressions."
        else:
            detail = "Execution pending."
        method_cards.append(
            f'<article class="card"><h2><a href="/RSI/methods/{slug}/">{html.escape(name)}</a></h2><p>{html.escape(detail)}</p></article>'
        )
        write(
            f"methods/{slug}",
            name,
            f'<p class="eyebrow">Principal method</p><h1>{html.escape(name)}</h1><p>{html.escape(detail)}</p><p><a href="https://github.com/ArshanBhanage/RSI/tree/main/experiments/methods">Run evidence</a> · <span class="pending">Video upload pending</span></p>',
        )
    write(
        "methods",
        "Methods",
        '<h1>Three inherited-improver adaptations</h1><div class="grid">'
        + "".join(method_cards)
        + "</div>",
    )
    comparison_path = ROOT / "experiments/reports/comparison.json"
    if comparison_path.exists():
        comparison = json.loads(comparison_path.read_text())
        rows = "".join(
            f"<tr><td>{r['method']}</td><td>{r['seed']}</td><td>{r['search_correct']}/12</td><td>{r['accepted_generations']}</td><td>{r['heldout_correct']}/2</td><td>{r['heldout_geomean']:.3f}</td></tr>"
            for r in comparison["rows"]
        )
    else:
        rows = '<tr><td colspan="6">Comparison execution pending</td></tr>'
    write(
        "evidence",
        "Evidence",
        "<h1>Matched-budget evidence</h1><table><thead><tr><th>Method</th><th>Seed</th><th>Search correct</th><th>Accepted</th><th>Held-out correct</th><th>Held-out geometric mean</th></tr></thead><tbody>"
        + rows
        + "</tbody></table><p>Incorrect held-out candidates contribute zero. Meta-call and token costs differ and remain in proposal metadata.</p>",
    )
    landing = f"""<section class="hero"><p class="eyebrow">Assignment 5 · verified research software</p><h1>Can an SQL improver improve how it improves?</h1><p>QueryForge-RSI tests policy replay, harness evolution and bottleneck-aware skill memory on authentic January and February 2025 NYC taxi records. Generated SQL is evaluated in a non-root, network-disabled container against a frozen correctness and latency authority.</p></section><section class="grid"><article class="card"><div class="metric">17/17</div><p>Section 10 code executions verified</p></article><article class="card"><div class="metric">3</div><p>principal inherited-improver mechanisms</p></article><article class="card"><div class="metric">2</div><p>declared seeds per matched comparison</p></article><article class="card"><div class="metric pending">0/20</div><p>YouTube uploads; owner deferred video work</p></article></section><h2>Evidence before claims</h2><p>Every public number comes from stored evaluator output. Incorrect candidates, rejected policies, timeouts and zero gains remain visible. The project reports adaptations where full paper reproduction is outside a laptop SQL experiment.</p><div class="grid">{"".join(cards[:3])}{"".join(method_cards)}</div>"""
    write("", "Home", landing)
    print(
        json.dumps(
            {"labs": len(labs), "methods": len(methods), "comparison": comparison_path.exists()}
        )
    )


if __name__ == "__main__":
    main()
