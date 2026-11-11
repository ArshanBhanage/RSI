"""A restrictive SQL language boundary, backed by disabled DuckDB external access."""

import sqlglot
from sqlglot import exp

SAFE_FUNCTIONS = {
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "MEDIAN",
    "EXTRACT",
    "DATE_TRUNC",
    "TIMESTAMP_TRUNC",
    "CAST",
    "TRY_CAST",
    "COALESCE",
    "IF",
    "NULLIF",
    "ABS",
    "FLOOR",
    "CEIL",
    "ROUND",
    "QUANTILE_CONT",
    "STRFTIME",
    "DAY",
    "MONTH",
    "YEAR",
    "HOUR",
    "DAY_OF_WEEK",
    "DATE",
    "INT_DIV",
}


def validate(sql: str) -> None:
    if len(sql) > 20000:
        raise ValueError("SQL size budget exceeded")
    trees = sqlglot.parse(sql, read="duckdb")
    if len(trees) != 1 or not isinstance(trees[0], (exp.Select, exp.Union)):
        raise ValueError("Only one SELECT query is permitted")
    tree = trees[0]
    names = {"trips", "zones"} | {x.alias.lower() for x in tree.find_all(exp.CTE)}
    for table in tree.find_all(exp.Table):
        if not isinstance(table.this, exp.Identifier) or table.db or table.catalog:
            raise ValueError("External or qualified table access denied")
        if table.name.lower() not in names:
            raise ValueError("Table outside workload denied")
    for func in tree.find_all(exp.Func):
        if isinstance(func, exp.Anonymous) or func.sql_name() not in SAFE_FUNCTIONS:
            raise ValueError(f"Function denied: {func.sql_name()}")
    forbidden = (
        exp.Command,
        exp.Insert,
        exp.Delete,
        exp.Update,
        exp.Create,
        exp.Drop,
        exp.Into,
        exp.Parameter,
    )
    if any(isinstance(node, forbidden) for node in tree.walk()):
        raise ValueError("Non-query construct denied")
