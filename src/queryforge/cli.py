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
