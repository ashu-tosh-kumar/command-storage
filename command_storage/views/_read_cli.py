import os
from datetime import datetime
from pathlib import Path

import typer
from tabulate import tabulate

from command_storage.controller.app import get_cmds
from command_storage.initializer import app
from command_storage.models.enums import arguments as arguments_enums
from command_storage.models.enums import error as error_enums

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
    """Show list of all stored commands. Also supports fuzzy matching on key. Run 'cmds
    list --help' to see how."""
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
    table = []
    headers = ["Key", "Command", "Description"]
    terminal_width_columns: int = os.get_terminal_size().columns

    for key, command in all_commands.commands.items():
        _command = command.command
        description = command.description
        row = [f"'{key}'", f"'{_command}'", f"'{description}'" if description else ""]
        table.append(row)

    typer.secho(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            maxcolwidths=[int(terminal_width_columns // 4), int(terminal_width_columns // 4), int(terminal_width_columns // 4)],
        ),
        fg=typer.colors.CYAN,
    )


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
            f"Successfully exported file to path: {file}: '{export_error}'",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f"Exporting file to path: {file} failed with '{export_error}'",
            fg=typer.colors.RED,
        )
