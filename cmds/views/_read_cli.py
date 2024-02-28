import typer

from cmds.controller.cmds import get_cmds
from cmds.models.enums import error as error_enums
from cmds.views.cli import app


def _list_callback(value: bool) -> None:
    """List callback

    Args:
        value (bool): Boolean value for whether to provide list or not

    Raises:
        typer.Exit: Raised to cleanly exit the CLI application
    """
    if value:
        typer.echo("")
        raise typer.Exit()


@app.command()
def list() -> None:
    """Show list of all stored commands."""
    cmds = get_cmds()
    all_commands = cmds.list()

    if all_commands.error != error_enums.Error.SUCCESS:
        typer.secho(f"Error in fetching commands: '{all_commands.error}'", fg=typer.colors.RED)
        raise typer.Exit(1)

    if len(all_commands.commands) == 0:
        typer.secho("There are no commands in cmds", fg=typer.colors.RED)
        raise typer.Exit()

    # echo commands
    columns = (
        "Key  ",
        "| Command  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for key, command in all_commands.commands.items():
        _command = command.command
        description = command.description
        typer.secho(
            f"{key}{(len(columns[0]) - len(str(id))) * ' '}" + f"| ({_command}){(len(columns[1]) - len(str(_command)) - 4) * ' '}" + f"| {description}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
