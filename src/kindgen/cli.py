"""This module provides the RP To-Do CLI."""

from pathlib import Path
from typing import List, Optional

import typer

from kindgen import __app_name__, __version__, configinit, templates

app = typer.Typer()
tpl = templates.Templates()

@app.command(
    help="Creates a directory with configuration file."
)
def init(dest_dir: str) -> None:
    init = configinit.ConfigInit(tpl.get_tpl_path(), dest_dir)
    error = init.prepare_dest_dir()
    if error:
        typer.secho(
            f'{error}', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    error = init.create_content()
    if error:
        typer.secho(
            f'{error}', fg=typer.colors.RED
        )
        raise typer.Exit(1)
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
