from datetime import datetime
from pathlib import Path

import typer
from prettytable.colortable import ColorTable, Themes

from cmds.controller.cmds import get_cmds
from cmds.models.enums import arguments as arguments_enums
from cmds.models.enums import error as error_enums
from cmds.views.cli import app

DEFAULT_FILE_LOCATION = Path().joinpath(f"command_storage_export_{datetime.now()}.json")

_INITIAL_KEY = typer.Option(
    None,
    arguments_enums.Arguments.KEY.value.long,
    arguments_enums.Arguments.KEY.value.short,
    help=arguments_enums.Arguments.KEY.value.description,
)
_INITIAL_FILE = typer.Option(
    DEFAULT_FILE_LOCATION,
    arguments_enums.Arguments.FILE.value.long,
    arguments_enums.Arguments.FILE.value.short,
    help=arguments_enums.Arguments.FILE.value.description,
)


@app.command()
def list(key: str = _INITIAL_KEY) -> None:
    """Show list of all stored commands or list of commands matching passed key."""
    cmds = get_cmds()

    if key:
        all_commands = cmds.list_fuzzy(key)
    else:
        all_commands = cmds.list()

    if all_commands.error != error_enums.Error.SUCCESS:
        typer.secho(f"Error in fetching commands: '{all_commands.error}'", fg=typer.colors.RED)
        raise typer.Exit(1)

    if len(all_commands.commands) == 0:
        if key:
            msg = f"There are no commands in cmds matching with {key}"
        else:
            msg = "There are no commands in cmds"
        typer.secho(msg, fg=typer.colors.RED)
        raise typer.Exit()

    # echo commands
    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["S/No.", "Key", "Command", "Description"]

    for idx, (key, command) in enumerate(all_commands.commands.items()):
        _command = command.command
        description = command.description
        table.add_row([idx + 1, key, _command, description])

    typer.secho(table)


@app.command()
def export(file: str = _INITIAL_FILE) -> None:
    """Exports all stored commands into a JSON file."""
    cmds = get_cmds()
    all_commands = cmds.list()

    if all_commands.error != error_enums.Error.SUCCESS:
        typer.secho(f"Error in fetching commands: '{all_commands.error}'", fg=typer.colors.RED)
        raise typer.Exit(1)

    if len(all_commands.commands) == 0:
        msg = "There are no commands in cmds"
        typer.secho(msg, fg=typer.colors.RED)
        raise typer.Exit()

    export_error = cmds.export_json(all_commands, file)

    if export_error == error_enums.Error.SUCCESS:
        typer.secho(
            f'Successfully exported file to path: {file}: "{export_error}"',
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f'Exporting file to path: {file} failed with "{export_error}"',
            fg=typer.colors.RED,
        )
