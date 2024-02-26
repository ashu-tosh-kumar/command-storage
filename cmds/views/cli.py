"""This module provides the commands-store CLI."""

# cmds/views/cli.py
from typing import Optional

import typer

from cmds import __app_name__, __version__

app = typer.Typer()


def _version_callback(value: bool) -> None:
    """Version callback

    Args:
        value (bool): Boolean value for whether to provide version or not

    Raises:
        typer.Exit: Raised to cleanly exit the CLI application
    """
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version.",
        callback=_version_callback,
        is_eager=True,  # takes precedence over other commands in current application
    )
) -> None:
    """_summary_

    Args:
        version (bool | None, optional): _description_. Defaults to typer.Option( None, "--version", "-v", help="Show the application's version.", callback=_version_callback, is_eager=True,  # takes precedence over other commands in current application ).
    """
    return
