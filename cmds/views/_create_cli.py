from typing import Optional

import typer
from typing_extensions import Annotated

from cmds.controller.cmds import get_cmds
from cmds.models.enums import arguments as arguments_enums
from cmds.models.enums import error as error_enums
from cmds.views.cli import app

_INITIAL_DESCRIPTION = typer.Option(
    None,
    arguments_enums.Arguments.DESCRIPTION.value.long,
    arguments_enums.Arguments.DESCRIPTION.value.short,
    help=arguments_enums.Arguments.DESCRIPTION.value.description,
)


@app.command()
def store(
    key: Annotated[
        str,
        typer.Option(
            arguments_enums.Arguments.KEY.value.long,
            arguments_enums.Arguments.KEY.value.short,
            help=arguments_enums.Arguments.KEY.value.description,
        ),
    ],
    command: Annotated[
        str,
        typer.Option(
            arguments_enums.Arguments.COMMAND.value.long,
            arguments_enums.Arguments.COMMAND.value.short,
            help=arguments_enums.Arguments.COMMAND.value.description,
        ),
    ],
    description: Optional[str] = _INITIAL_DESCRIPTION,
) -> None:
    """Store a new command into cmds."""
    cmds = get_cmds()
    commands = cmds.add(key, command, description)

    if commands.error != error_enums.Error.SUCCESS:
        typer.secho(
            message=f'Error in storing the command "{commands.error}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    typer.secho(
        message=f'Successfully stored the new command: "{commands.error}"',
        fg=typer.colors.GREEN,
    )
