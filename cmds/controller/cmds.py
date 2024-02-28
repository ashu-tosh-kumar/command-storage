from pathlib import Path
from typing import Optional

import typer
from thefuzz import process

from cmds.controller import config
from cmds.models.database import db_models
from cmds.models.database.json_wrapper import JsonWrapper, get_database_path
from cmds.models.enums import error as error_enums


class Cmds:
    """Application Controller"""

    def __init__(self, db_path: Path) -> None:
        """Initializer for `Cmds`

        Args:
            db_path (Path): DB path for storing database file
        """
        self._db_handler = JsonWrapper(db_path)

    def list(self) -> db_models.Commands:
        """Interface to get list of all stored commands from database

        Returns:
            db_models.Commands: Returns all commands model
        """
        commands = self._db_handler.get_commands()

        return commands

    def list_fuzzy(self, key: str, limit: int = 5) -> db_models.Commands:
        """Interface to get list of all stored commands from database

        Args:
            key (str): Key for fuzzy matching.
            limit (int, optional): Maximum no. of records to return. Defaults to 5.

        Returns:
            db_models.Commands: Returns all commands model.
        """
        commands = self._db_handler.get_commands()
        fuzzy_commands = db_models.Commands(commands={}, error=commands.error)

        choices = list(commands.commands.keys())
        extract_list = process.extract(key, choices, limit=limit)

        for extract in extract_list:
            _key = extract[0]
            fuzzy_commands.commands[_key] = commands.commands[_key]

        return fuzzy_commands

    def add(self, key: str, command: str, description: Optional[str]) -> db_models.Commands:
        """Interface to store a new command into the database.

        Args:
            key (str): Key for the new command to be stored.
            command (str): Command to be stored.
            description (Optional[str]): Description for command to be stored.

        Returns:
            db_models.Commands: Returns updated list of commands stored.
        """
        commands = self._db_handler.get_commands()

        if key in commands.commands:
            return db_models.Commands(commands={}, error=error_enums.Error.KEY_ERROR)

        new_command = db_models.Command(key=key, command=command, description=description)

        commands.commands[key] = new_command
        commands = self._db_handler.write_commands(commands)

        return commands


def get_cmds() -> Cmds:
    """Returns an instance of `Cmds` with checks for various paths and config file(s).

    Raises:
        typer.Exit: Raised if config file path is not found.
        typer.Exit: Raised if db path is not found.

    Returns:
        Cmds: Returns an instance of `Cmds`.
    """
    if config.CONFIG_FILE_PATH.exists():
        db_path = get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            message=f"Config file: '{config.CONFIG_FILE_PATH}' not found. Please, run 'cmds init'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if db_path.exists():
        return Cmds(db_path)
    else:
        typer.secho(
            message=f"Database file: '{db_path}' not found. Please, run 'cmds init'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
