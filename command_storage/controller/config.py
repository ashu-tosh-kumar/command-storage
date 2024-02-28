import configparser
from pathlib import Path

import typer

from command_storage.models.constants import APP_NAME
from command_storage.models.enums import error as error_enums

CONFIG_DIR_PATH = Path(typer.get_app_dir(APP_NAME))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def _initialize_config_file() -> error_enums.Error:
    """Initializes the config file. If the config file doesn't already exists, it
    creates the required directory as well as the config file

    Returns:
        error_enums.Error: Returns the error code
    """
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return error_enums.Error.DIR_ERROR

    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return error_enums.Error.FILE_ERROR

    return error_enums.Error.SUCCESS


def _create_database_config(db_path: Path) -> error_enums.Error:
    """Creates database config in the config file

    Args:
        db_path (Path): Path for database file

    Returns:
        error_enums.Error: Returns the error code
    """
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": str(db_path)}

    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return error_enums.Error.DB_WRITE_ERROR

    return error_enums.Error.SUCCESS


def initialize_app(db_path: Path) -> error_enums.Error:
    """Initializes the Cmds application

    Args:
        db_path (Path): DB path for database file

    Returns:
        error_enums.Error: Returns the error code
    """
    config_code = _initialize_config_file()
    if config_code != error_enums.Error.SUCCESS:
        return config_code

    database_code = _create_database_config(db_path)
    if database_code != error_enums.Error.SUCCESS:
        return database_code

    return error_enums.Error.SUCCESS
