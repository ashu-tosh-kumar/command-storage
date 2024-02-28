from enum import Enum

from cmds.models.models import error as error_model


class Error(Enum):
    SUCCESS = error_model.Error(code=0, name="SUCCESS", description="transaction successful")
    DIR_ERROR = error_model.Error(code=1, name="DIR_ERROR", description="config directory error")
    FILE_ERROR = error_model.Error(code=2, name="FILE_ERROR", description="config file error")
    DB_READ_ERROR = error_model.Error(code=3, name="DB_READ_ERROR", description="database read error")
    DB_WRITE_ERROR = error_model.Error(code=4, name="DB_WRITE_ERROR", description="database write error")
    JSON_ERROR = error_model.Error(code=5, name="JSON_ERROR", description="database file corruption")
    KEY_ERROR = error_model.Error(code=6, name="KEY_ERROR", description="Duplicate key issue")

    def __str__(self) -> str:
        """User friendly print output

        Returns:
            str: Returns string representation of the enum
        """
        return f"{self.value.name}: {self.value.description}"


ERROR_CODE_TO_NAME_MAPPING = {enum.value.code: enum for enum in Error}
