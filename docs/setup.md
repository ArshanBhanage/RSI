# Setup and reproduction

Requirements: macOS with `uv`, Docker Desktop, Git, authenticated `codex` CLI and about 250 MB free for environments plus 120 MB for TLC data.

```sh
uv sync --locked
cp .env.example .env && chmod 600 .env
docker build -t queryforge-eval:v1 sandbox
uv run queryforge doctor
uv run queryforge data fetch
uv run queryforge data verify
uv run pytest -q
```

Model experiments consume authenticated provider capacity and are intentionally absent from CI. Reports already committed under `experiments/` can be audited without credentials. Lesson reports are immutable; use a separate checkout for a new experiment series.
