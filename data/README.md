# Authentic NYC TLC data

`uv run queryforge data fetch` downloads January and February 2025 Yellow Taxi records and the official zone lookup directly from links on the [TLC data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The initial retrieval establishes SHA-256 pins in `manifests/tlc.json`; later runs refuse changed bytes. `uv run queryforge data verify` checks every local file. Offline mode never creates new provenance or substitutes data.

The manifest records actual retrieval timestamps, sizes, row counts and Arrow schema. Raw files are excluded from Git. Hashes are local retrieval pins, not publisher-signed checksums. TLC warns that vendor-supplied records may be inaccurate. Public access does not imply a new software license; consult [NYC terms](https://www.nyc.gov/home/terms-of-use.page) and the publisher's documentation for reuse.

January is used for development and selection. February is held out from search; its metadata may be inspected for schema and integrity, but query answers and performance feedback must not enter optimization.

Workload semantics are fixed in `experiments/workload/queries.json`: preserve all raw records, including anomalous dates and negative financial adjustments. Only q03 filters negative distance. SQL NULL aggregate semantics apply. Missing zones remain a NULL borough in the left join. q05 means day-of-month <= 7, including out-of-month records. q08 uses three observed dates, not three consecutive calendar dates. Quantiles use exact DuckDB median with numeric tolerance 1e-8 absolute/1e-7 relative. No fabricated trip fixtures are used.
