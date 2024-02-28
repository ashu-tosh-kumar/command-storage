"""Defines Read arguments for the application
"""

from enum import Enum

from command_storage.models.models import argument as argument_model


class Arguments(Enum):
    """Arguments for various commands"""

    DB_PATH = argument_model.Argument(short="-db", long="--db-path", type=str, description="Database file path.")
    VERSION = argument_model.Argument(short="-v", long="--version", type=str, description="Show cmds version.")
    KEY = argument_model.Argument(short="-k", long="--key", type=str, description="Key for the command.")
    COMMAND = argument_model.Argument(short="-c", long="--command", type=str, description="Command to be stored.")
    DESCRIPTION = argument_model.Argument(short="-des", long="--description", type=str, description="Description of command to be stored.")
    FILE = argument_model.Argument(short="-f", long="--file", type=str, description="Export file address with extension")
    ALL = argument_model.Argument(short="-a", long="--all", type=str, description="Delete all commands")
