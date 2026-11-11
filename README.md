# QueryForge-RSI

An assignment implementation investigating recursive improvement of SQL-search procedures over authentic NYC TLC trip records.

**Status: M00 in progress. No SQL experiment, codelab or RSI method is verified yet.**

- [Pinned course sources and 17-lab mapping](docs/references/source-lock.md)
- [Method fidelity and release audit](research/method-fidelity.md)
- [Milestone gates](docs/milestones.md)
- [Delivery status](docs/delivery-status.md)

Run the implemented source-integrity check with Python 3:

```sh
python3 scripts/verify_sources.py
```

The command downloads immutable source files, checks SHA-256 hashes and validates all 17 lesson headings. `--offline` uses only hash-verified cached source bytes. It does not execute upstream synthetic demos or claim scientific results.

The destination is [ArshanBhanage/RSI](https://github.com/ArshanBhanage/RSI). Website and required lab/method videos are not published. Milestones proceed sequentially only after their recorded execution and publication gates pass.
