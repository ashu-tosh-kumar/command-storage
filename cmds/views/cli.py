"""This module provides the commands-store CLI."""

from pathlib import Path
from typing import Optional

import typer

from cmds import __app_name__, __version__
from cmds.controller import config
from cmds.models.database.json_wrapper import DEFAULT_DB_FILE_PATH, init_database
from cmds.models.enums import arguments as arguments_enums
from cmds.models.enums import error as error_enums

app = typer.Typer()

_INITIAL_DB_PATH = typer.Option(
    str(DEFAULT_DB_FILE_PATH),
    arguments_enums.Arguments.DB_PATH.value.long,
    arguments_enums.Arguments.DB_PATH.value.short,
    prompt=arguments_enums.Arguments.DB_PATH.value.description,
)


@app.command()
def init(
    db_path: str = _INITIAL_DB_PATH,
) -> None:
    """Initialize the application. One time process but can be safely run multiple
    times.

    Args:
        db_path (str, optional): `--db-path` argument. Defaults to _INITIAL_DB_PATH.

    Raises:
        typer.Exit: If error in app initialization
        typer.Exit: if error in database file initialization
    """
    db_path_obj = Path(db_path)

    # Initialize application
    app_init_error = config.initialize_app(db_path_obj)
    if app_init_error != error_enums.Error.SUCCESS:
        typer.secho(
            f'Creating config file failed with "{app_init_error}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Initialize database file
    db_init_error = init_database(Path(db_path_obj))
    if db_init_error != error_enums.Error.SUCCESS:
        typer.secho(
            f'Creating database failed with "{db_init_error}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The cmds is successfully initialized '{db_path_obj};", fg=typer.colors.GREEN)


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


_INITIAL_VERSION = typer.Option(
    None,
    arguments_enums.Arguments.VERSION.value.long,
    arguments_enums.Arguments.VERSION.value.short,
    help=arguments_enums.Arguments.VERSION.value.description,
    callback=_version_callback,
    is_eager=True,  # takes precedence over other commands in current application
)


@app.callback()
def version(version: Optional[bool] = _INITIAL_VERSION) -> None:
    pass
