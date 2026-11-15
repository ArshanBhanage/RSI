# Submission

- Repository: <https://github.com/ArshanBhanage/RSI>
- Website: <https://arshanbhanage.github.io/RSI/>
- Data: official NYC TLC yellow taxi January/February 2025 Parquet; hashes in `data/manifests/tlc.json`
- Comparison: `experiments/reports/comparison.json`
- Videos: 0/20 uploaded; owner deferred recording/upload
- Verified publication commit: `d202f3114aaf53d6556cbc4714ab63791c761285`
- Passing CI: <https://github.com/ArshanBhanage/RSI/actions/runs/43668922361>
- Passing Pages deployment: <https://github.com/ArshanBhanage/RSI/actions/runs/43668922412>

Run `uv sync --locked && uv run pytest -q && uv run ruff check . && uv run mypy src && bash scripts/check_delivery.sh`. Live model reruns also require authenticated Codex CLI capacity and Docker. The comparison reports zero accepted recursive-improver generations and retains regressions and failures.
