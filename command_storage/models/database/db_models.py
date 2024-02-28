from typing import Optional, Union

from pydantic import BaseModel, field_serializer, validator

from command_storage.models.enums import error as error_enums


class Command(BaseModel):
    """Model for a command"""

    key: str  # key to store with
    command: str  # command to store with
    description: Optional[str] = None  # description of command


class Commands(BaseModel):
    """Model for the whole database to store all commands"""

    commands: dict[str, Command]
    error: error_enums.Error

    @field_serializer("error")
    def serialize_dt(self, error: Union[error_enums.Error, int], _info) -> int:
        """Custom serializer for `error`

        Args:
            error (Union[error_enums.Error, int]): Error
            _info (_type_): _description_

        Returns:
            int: JSON serializer for `error`
        """
        if isinstance(error, error_enums.Error):
            return error.value.code

        return error

    @validator("error", pre=True)
    def convert_int_into_error_enum(cls, value: Union[error_enums.Error, int]) -> error_enums.Error:
        """Handles the int error and converts into `error_enums.Error`

        Args:
            value (Union[error_enums.Error, int]): Input value

        Returns:
            error_enums.Error: Converted value if input value is `int`
        """
        if isinstance(value, int):
            return error_enums.ERROR_CODE_TO_NAME_MAPPING[value]

        return value
