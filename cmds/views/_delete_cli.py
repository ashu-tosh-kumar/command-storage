from typing import Optional

import typer

from cmds.controller.app import get_cmds
from cmds.initializer import app
from cmds.models.enums import arguments as arguments_enums
from cmds.models.enums import error as error_enums

_INITIAL_DELETE_ALL = typer.Option(
    False,
    arguments_enums.Arguments.ALL.value.long,
    arguments_enums.Arguments.ALL.value.short,
    help=arguments_enums.Arguments.ALL.value.description,
)


def _validate_delete_options(key: Optional[str], delete_all: bool) -> None:
    """Custom validator for `delete` command arguments and options

    Args:
        key (Optional[str]): Key argument
        delete_all (bool): `--all` option

    Raises:
        typer.BadParameter: Raised if neither `key` argument not `-all` option are
        passed.
    """
    if not key and not delete_all:
        raise typer.BadParameter("Either provide a key or use '--all' option to delete all stored commands.")


@app.command()
def delete(key: Optional[str] = typer.Argument(None), delete_all: bool = _INITIAL_DELETE_ALL) -> None:
    """Allows deletion of stored command by key"""
    _validate_delete_options(key, delete_all)

    cmds = get_cmds()
    delete_error = cmds.delete(key, delete_all)

    if delete_error == error_enums.Error.SUCCESS:
        if delete_all:
            msg = "Successfully deleted all stored commands"
        else:
            msg = f"Successfully deleted key: '{key}': '{delete_error}'"
        typer.secho(
            msg,
            fg=typer.colors.GREEN,
        )
    else:
        if delete_all:
            msg = "Error in deleting all stored commands: '{delete_error}'"
        else:
            msg = f"Error in deleting key: '{key}': '{delete_error}'"
        typer.secho(
            msg,
            fg=typer.colors.RED,
        )
