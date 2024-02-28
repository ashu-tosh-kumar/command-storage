"""This module provides the commands-store CLI."""

from pathlib import Path
from typing import Optional

import typer

from command_storage.controller import config
from command_storage.initializer import app
from command_storage.models.constants import APP_NAME, VERSION
from command_storage.models.database.json_wrapper import (
    DEFAULT_DB_FILE_PATH,
    init_database,
)
from command_storage.models.enums import arguments as arguments_enums
from command_storage.models.enums import error as error_enums
from command_storage.views._create_cli import *  # noqa: F401 # NOSONAR
from command_storage.views._delete_cli import *  # noqa: F401 # NOSONAR
from command_storage.views._read_cli import *  # noqa: F401 # NOSONAR
from command_storage.views._update_cli import *  # noqa: F401 # NOSONAR

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
    """Initialize the application. One time process and overwrites existing config and
    data files.

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
            f"Creating config file failed with '{app_init_error}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Initialize database file
    db_init_error = init_database(Path(db_path_obj))
    if db_init_error != error_enums.Error.SUCCESS:
        typer.secho(
            f"Creating database failed with '{db_init_error}'",
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
        typer.secho(f"{APP_NAME} v{VERSION}", fg=typer.colors.CYAN)
        raise typer.Exit()

    typer.secho("Welcome to command-storage. Run 'cmds --help' to get help.", fg=typer.colors.CYAN)


_INITIAL_VERSION = typer.Option(
    None,
    arguments_enums.Arguments.VERSION.value.long,
    arguments_enums.Arguments.VERSION.value.short,
    help=arguments_enums.Arguments.VERSION.value.description,
    callback=_version_callback,
    is_eager=True,  # takes precedence over other commands in current application
)


@app.callback(invoke_without_command=True)
def version(version: Optional[bool] = _INITIAL_VERSION) -> None:
    pass


if __name__ == "__main__":
    app(prog_name=APP_NAME)
