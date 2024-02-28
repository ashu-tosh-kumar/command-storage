"""Defines Read arguments for the application
"""

from enum import Enum

from cmds.models.models import argument as argument_model


class Arguments(Enum):
    """Arguments for various commands"""

    DB_PATH = argument_model.Argument(short="-db", long="--db-path", type=str, description="Database file path.")
    VERSION = argument_model.Argument(short="-v", long="--version", type=str, description="Show cmds version.")
    KEY = argument_model.Argument(short="-k", long="--key", type=str, description="Key for the command to be stored.")
    COMMAND = argument_model.Argument(short="-c", long="--command", type=str, description="Command to be stored.")
    DESCRIPTION = argument_model.Argument(short="-description", long="--description", type=str, description="Description of command to be stored.")

    EXPORT = argument_model.Argument(short="-e", long="--export", type=str, description="Export stored commands to a file.")
    UPDATE = argument_model.Argument(
        short="-u",
        long="--update",
        type=str,
        description="Update an existing command",
    )
    DELETE = argument_model.Argument(short="-d", long="--delete", type=str, description="Delete an existing command")
