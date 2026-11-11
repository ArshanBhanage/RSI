# Initial setup inventory

Observed during M00 on macOS arm64: system Python 3.9.6 (below project target); Homebrew Python 3.13.18 available through uv; uv 0.12.10; FFmpeg/ffprobe 8.0.1; git, gh, Codex CLI, Docker CLI, Node and npm present. asciinema, VHS and Gemini CLI were not found on PATH. Docker daemon and coding-agent authentication are not yet tested.

GitHub CLI authenticated to ArshanBhanage with repo/workflow scopes. The destination was empty when cloned. YouTube Studio sign-in was observed on November 6; upload verification remains pending.

M00 source verifier uses the Python standard library. Its video renderer uses uv with inline pinned Pillow 11.3.0 and Pygments 2.19.2, plus FFmpeg and the macOS Menlo font. The renderer captures executed subprocess output and actual source bytes, then composes paginated frames with reading pauses. This is not an unedited desktop recording. No narration is claimed.

The full Python project lockfile and sandbox setup belong to M01. Empty `.env` and `.env.example` files exist with mode 0600. `.env`, raw datasets, local caches and video renders are gitignored.
