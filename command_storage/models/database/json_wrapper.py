import configparser
import json
from pathlib import Path

from command_storage.models.database import db_models
from command_storage.models.enums import error as error_enums
from command_storage.models.enums import error as error_model

DEFAULT_DB_FILE_PATH = Path.home().joinpath("." + Path.home().stem + "_cmds.json")


def init_database(db_path: Path) -> error_model.Error:
    """Create the Cmds database

    Args:
        db_path (Path): Path to database file

    Returns:
        error_model.Error: Returns error code
    """
    try:
        db_path.write_text("{}")  # Empty cmds dictionary
        return error_model.Error.SUCCESS
    except OSError:
        return error_model.Error.DB_WRITE_ERROR


def get_database_path(config_file: Path) -> Path:
    """Returns the current path to the database

    Args:
        config_file (Path): Path to the config file

    Returns:
        Path: Path to the database file as read from config file
    """
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


class JsonWrapper:
    def __init__(self, db_path: Path) -> None:
        """Initializer for `JsonWrapper`

        Args:
            db_path (Path): Path of JSON file to be used as database
        """
        self._db_path = db_path

    def get_commands(self) -> db_models.Commands:
        """Reads all stored commands and return the same

        Returns:
            db_models.Commands: Returns the read command as `db_models.Commands`
        """
        try:
            with self._db_path.open("r") as db:
                try:
                    json_data = json.load(db)
                    return db_models.Commands(commands=json_data.get("commands", {}), error=error_enums.Error.SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return db_models.Commands(commands={}, error=error_enums.Error.JSON_ERROR)
        except OSError:  # Catch file IO problems
            return db_models.Commands(commands={}, error=error_enums.Error.DB_READ_ERROR)

    def write_commands(self, commands: db_models.Commands) -> db_models.Commands:
        """Stores new list of commands into the database

        Args:
            commands (db_models.Commands): New commands object

        Returns:
            db_models.Commands: Returns back the updated list of commands
        """
        try:
            with self._db_path.open("w") as db:
                json.dump(commands.model_dump(), db, indent=4)
            return db_models.Commands(commands={}, error=error_enums.Error.SUCCESS)
        except OSError:  # Catch file IO problems
            return db_models.Commands(commands={}, error=error_enums.Error.DB_WRITE_ERROR)
