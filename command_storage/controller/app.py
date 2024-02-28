import json
from pathlib import Path
from typing import Optional

import typer
from thefuzz import process

from command_storage.controller import config
from command_storage.models.database import db_models
from command_storage.models.database.json_wrapper import JsonWrapper, get_database_path
from command_storage.models.enums import error as error_enums


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
            return db_models.Commands(commands={}, error=error_enums.Error.DUPLICATE_KEY_ERROR)

        new_command = db_models.Command(key=key, command=command, description=description)

        commands.commands[key] = new_command
        commands = self._db_handler.write_commands(commands)

        return commands

    def export_json(self, all_commands: db_models.Commands, export_file: str) -> error_enums.Error:
        """Exports the json data into given export file

        Args:
            all_commands (db_models.Commands): Json data that needs to be exported
            export_file (str): File into which data needs to be exported

        Returns:
            error_enums.Error: Returns error code of the operation
        """
        try:
            json_data = [command.model_dump() for command in all_commands.commands.values()]

            with Path(export_file).open("w") as f:
                json.dump(json_data, f, indent=4)
                return error_enums.Error.SUCCESS
        except OSError:  # Catch file IO problems
            return error_enums.Error.JSON_EXPORT_FILE_ERROR

    def update(self, orig_key: str, new_key: Optional[str], command: Optional[str], description: Optional[str]) -> error_enums.Error:
        """Allows updating an existing command including (optionally) its key

        Args:
            orig_key (str): Key for which update needs to happen
            new_key (Optional[str]): New key if key needs to be changed
            command (Optional[str]): New command
            description (Optional[str]): New description

        Returns:
            error_enums.Error: Returns error code of the operation
        """
        commands = self._db_handler.get_commands()

        if orig_key not in commands.commands:
            return error_enums.Error.NON_EXISTENT_KEY_ERROR

        command_obj = commands.commands[orig_key]

        # Update command
        if command is not None:
            command_obj.command = command

        # Update description
        if description is not None:
            command_obj.description = description

        # Update the key
        if new_key is not None:
            # insert new key and remove old one
            commands.commands.pop(orig_key)
            commands.commands[new_key] = command_obj
        else:
            commands.commands[orig_key] = command_obj

        commands = self._db_handler.write_commands(commands)
        return commands.error

    def delete(self, key: Optional[str], delete_all: bool) -> error_enums.Error:
        """Allows deleting a stored command by it's key

        Args:
            key (Optional[str]): Key that needs to be deleted
            delete_all (bool): Whether to delete all items

        Returns:
            error_enums.Error: Returns error code of operation
        """
        # -- DELETE ALL DATA --
        if delete_all:
            empty_commands = db_models.Commands(commands={}, error=error_enums.Error.SUCCESS)
            commands = self._db_handler.write_commands(empty_commands)
            return commands.error

        commands = self._db_handler.get_commands()

        if key not in commands.commands:
            return error_enums.Error.NON_EXISTENT_KEY_ERROR

        commands.commands.pop(key)
        commands = self._db_handler.write_commands(commands)
        return commands.error


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
