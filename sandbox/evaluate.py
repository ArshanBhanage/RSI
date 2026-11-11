"""Immutable external authority. Only submitted SQL enters the SQL interpreter."""

import hashlib
import json
import math
import random
import resource
import statistics
import sys
import threading
import time
from pathlib import Path

import duckdb
from sqlglot.errors import SqlglotError

sys.path.insert(0, "/authority")
from sql_safety import validate


def canonical(rows):
    return sorted(rows, key=lambda row: tuple((x is not None, str(x)) for x in row))


def equivalent(left, right):
    if len(left) != len(right):
        return False
    for a, b in zip(canonical(left), canonical(right)):
        if len(a) != len(b):
            return False
        for x, y in zip(a, b):
            if isinstance(x, float) and isinstance(y, (int, float)):
                if not math.isfinite(x) or not math.isfinite(y):
                    if x != y:
                        return False
                elif not math.isclose(x, y, abs_tol=1e-8, rel_tol=1e-7):
                    return False
            elif x != y:
                return False
    return True


def timed(con, sql, timeout):
    timer = threading.Timer(timeout, con.interrupt)
    timer.start()
    start = time.perf_counter()
    try:
        cursor = con.execute(sql)
        rows = cursor.fetchall()
        schema = [(x[0], str(x[1])) for x in cursor.description]
        return time.perf_counter() - start, rows, schema
    finally:
        timer.cancel()


def main():
    request = json.load(sys.stdin)
    config = json.loads(Path("/authority/evaluation.json").read_text())
    queries = {q["id"]: q for q in json.loads(Path("/authority/queries.json").read_text())}
    con = duckdb.connect(config={"threads": config["threads"], "memory_limit": "1500MB"})
    con.execute("CREATE TABLE trips AS SELECT * FROM read_parquet('/data/trips.parquet')")
    con.execute("CREATE TABLE zones AS SELECT * FROM read_csv_auto('/data/zones.csv')")
    con.execute("SET enable_external_access = false")
    con.execute("SET lock_configuration = true")
    records = []
    rng = random.Random(request["seed"])
    for candidate in request["candidates"]:
        row = {"query_id": candidate["query_id"], "sql": candidate["sql"], "correct": False}
        try:
            query = queries[candidate["query_id"]]
            if query["partition"] == "heldout" and not request.get("final", False):
                raise ValueError("Held-out query denied during search")
            baseline = query["sql"]
            validate(candidate["sql"])
            validate(baseline)
            first, reference, reference_schema = timed(
                con, baseline, config["query_timeout_seconds"]
            )
            cold, result, schema = timed(con, candidate["sql"], config["query_timeout_seconds"])
            if reference_schema != schema or not equivalent(reference, result):
                raise ValueError("Semantic or schema mismatch")
            timings = {"baseline": [], "candidate": []}
            for _ in range(config["warm_repeats"]):
                order = ["baseline", "candidate"]
                rng.shuffle(order)
                for kind in order:
                    elapsed, result, schema = timed(
                        con,
                        baseline if kind == "baseline" else candidate["sql"],
                        config["query_timeout_seconds"],
                    )
                    if reference_schema != schema or not equivalent(reference, result):
                        raise ValueError("Repeated-run semantic mismatch")
                    timings[kind].append(elapsed)
            b, c = (statistics.median(timings[k]) for k in ["baseline", "candidate"])
            row.update(
                correct=True,
                baseline_median=b,
                candidate_median=c,
                speedup=b / c,
                warm_seconds=timings,
                first_query_seconds={"baseline": first, "candidate": cold},
                timing_caveat="First query is not an OS cold-cache measurement; data already loaded.",
                dispersion={k: statistics.pstdev(v) for k, v in timings.items()},
                rows=len(reference),
                schema=schema,
                result_sha256=hashlib.sha256(repr(canonical(reference)).encode()).hexdigest(),
                plan=con.execute("EXPLAIN " + candidate["sql"]).fetchall()[0][1],
            )
        except (ValueError, duckdb.Error, SqlglotError) as error:
            row.update(error_category=type(error).__name__, error=str(error), speedup=0)
        records.append(row)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(
        json.dumps(
            {
                "records": records,
                "engine": duckdb.__version__,
                "peak_rss_kb": usage.ru_maxrss,
                "cpu_seconds": usage.ru_utime + usage.ru_stime,
            },
            default=str,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
