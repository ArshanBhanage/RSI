import json

import pytest
from sqlglot.errors import SqlglotError

from queryforge.provenance import ROOT
from queryforge.sql_safety import validate


@pytest.mark.parametrize(
    "sql",
    [
        "COPY trips TO '/tmp/stolen.csv'",
        "SELECT * FROM read_csv('/etc/passwd')",
        "SELECT * FROM information_schema.tables",
        "SELECT 1; SELECT 2",
        "ATTACH '/tmp/other.db'",
        "INSTALL httpfs",
        "SELECT getenv('HOME')",
        "SELECT * INTO stolen FROM trips",
        "SELECT * FROM '/etc/passwd'",
        "SELECT system('fork')",
        "SELECT * FROM query('SELECT 1')",
    ],
)
def test_denied_sql(sql):
    with pytest.raises((ValueError, SqlglotError)):
        validate(sql)


def test_frozen_reference_language():
    for query in json.loads((ROOT / "experiments/workload/queries.json").read_text()):
        validate(query["sql"])
