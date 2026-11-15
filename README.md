# QueryForge-RSI

QueryForge-RSI asks whether an improver can improve **how it searches for correctness-preserving analytical SQL rewrites** under a fixed budget. It uses checksum-verified January and February 2025 NYC TLC yellow-taxi records, DuckDB, controlled real Codex CLI proposals and an immutable evaluator in a non-root, network-disabled Docker container.

The target artifact is SQL. Three meta-improver adaptations revise the search procedure for a later fresh generation: DREAM-RSI policy replay, AIDE²-inspired harness evolution and RSIFlow bottleneck/skill routing. Promotion requires correctness and at least 1.02× on both search tasks. Failed generations remain evidence.

## Reproduce

```sh
uv sync --locked
uv run queryforge doctor
uv run queryforge data fetch
uv run queryforge data verify
uv run queryforge benchmark baseline
uv run pytest -q
uv run queryforge compare --verify
bash scripts/check_delivery.sh
```

New model experiments require authenticated Codex CLI access and Docker. Existing reports can be audited offline. See [setup](docs/setup.md), [architecture](docs/architecture.md), [protocol](docs/evaluation-protocol.md), [method fidelity](research/method-fidelity.md), [results](research/results.md) and [delivery status](docs/delivery-status.md).

## Evidence map

- [17 Section 10 codelabs](codelabs) and their machine-readable [`experiments/labs`](experiments/labs)
- [DREAM-RSI](research/methods/dream_rsi), [AIDE² adaptation](research/methods/aide2), [RSIFlow](research/methods/rsiflow)
- [Matched comparison](experiments/reports/comparison.json)
- [Submission website](site)
- [Video manifest](videos/VIDEO_MANIFEST.json): owner deferred recording/upload; no YouTube completion is claimed

All 17 codelab code/evidence gates pass. The principal comparison uses three generations × four candidates for each of two seeds, plus one two-task held-out evaluation after freezing. Results retain regressions and correctness failures.

Repository: <https://github.com/ArshanBhanage/RSI> · Website: <https://arshanbhanage.github.io/RSI/>
