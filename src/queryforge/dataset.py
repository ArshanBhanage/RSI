"""Official TLC downloads, first-retrieval provenance, and pinned offline reuse."""

import json
import shutil
from urllib.request import urlopen

import pyarrow.parquet as pq

from .provenance import ROOT, digest, now, save

PUBLISHER = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
FILES = {
    "development": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet",
    "heldout": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-02.parquet",
    "zones": "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv",
}
MANIFEST = ROOT / "data/manifests/tlc.json"


def fetch(offline: bool = False) -> dict:
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    records = {}
    for role, url in FILES.items():
        path = ROOT / "data/raw" / url.rsplit("/", 1)[1]
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            if offline:
                raise FileNotFoundError(f"Offline file missing: {path.name}")
            temp = path.with_suffix(".part")
            with urlopen(url, timeout=60) as source, temp.open("wb") as target:
                shutil.copyfileobj(source, target)
            temp.replace(path)
        sha = digest(path)
        if role in previous and previous[role]["sha256"] != sha:
            raise ValueError(f"Pinned data changed: {role}")
        if role in previous:
            records[role] = previous[role]
            continue
        if offline:
            raise ValueError("Offline reuse requires a pre-existing provenance manifest")
        item = {
            "url": url,
            "publisher": PUBLISHER,
            "retrieved_utc": now(),
            "sha256": sha,
            "bytes": path.stat().st_size,
            "path": str(path.relative_to(ROOT)),
        }
        if path.suffix == ".parquet":
            meta = pq.ParquetFile(path)
            item["rows"] = meta.metadata.num_rows
            item["schema"] = str(meta.schema_arrow)
            required = {
                "tpep_pickup_datetime",
                "PULocationID",
                "DOLocationID",
                "trip_distance",
                "total_amount",
            }
            if not required.issubset(meta.schema_arrow.names):
                raise ValueError("TLC schema lacks workload columns")
        records[role] = item
    save(MANIFEST, records)
    return records


def verify() -> dict:
    records = fetch(offline=True)
    return {"passed": True, "files": {role: item["sha256"] for role, item in records.items()}}
