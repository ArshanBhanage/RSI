"""Reproducible entry points; missing prerequisites fail explicitly."""

import json

import typer

from . import environment

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main():
    """QueryForge evidence commands."""


@app.command()
def doctor():
    report = environment.check()
    print(json.dumps(report, indent=2))
    if not report["passed"]:
        raise typer.Exit(1)


from . import dataset

data_app = typer.Typer()
app.add_typer(data_app, name="data")


@data_app.command("fetch")
def data_fetch(offline: bool = False):
    print(json.dumps(dataset.fetch(offline), indent=2))


@data_app.command("verify")
def data_verify():
    print(json.dumps(dataset.verify(), indent=2))


from . import evaluator

benchmark_app = typer.Typer()
app.add_typer(benchmark_app, name="benchmark")


@benchmark_app.command("baseline")
def benchmark_baseline():
    print(json.dumps(evaluator.baseline(), indent=2))
