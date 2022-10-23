"""This module provides the RP To-Do CLI."""

from pathlib import Path
from typing import List, Optional

import typer

from kindgen import __app_name__, __version__

app = typer.Typer()

@app.command(
    help="Creates a directory with configuration file."
)
def init() -> None:
    return None

@app.command(
    help="Creates a new deployment based on an initalized directory."
)
def create() -> None:
    return None

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
