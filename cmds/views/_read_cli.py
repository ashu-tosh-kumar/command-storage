import typer
from prettytable.colortable import ColorTable, Themes

from cmds.controller.cmds import get_cmds
from cmds.models.enums import arguments as arguments_enums
from cmds.models.enums import error as error_enums
from cmds.views.cli import app

_INITIAL_KEY = typer.Option(
    None,
    arguments_enums.Arguments.KEY.value.long,
    arguments_enums.Arguments.KEY.value.short,
    help=arguments_enums.Arguments.KEY.value.description,
)


@app.command()
def list(key: str = _INITIAL_KEY) -> None:
    """Show list of all stored commands or list of commands matching passed keys."""
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
