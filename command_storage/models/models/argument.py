from pydantic import BaseModel, validator


class Argument(BaseModel):
    """Defined model for defining a CLI argument with both short and long types"""

    short: str  # must start with single dash (`-`)
    long: str  # must start with two dashes (`--`)
    type: type
    description: str

    @validator("short")
    def short_should_start_with_dash(cls, short: str) -> str:
        """Checks if short argument had a single dash `-` before it.

        Args:
            short (str): Input short value

        Raises:
            ValueError: Raised if short doesn't have `-` before it

        Returns:
            str: Returns short if it's valid
        """
        if not short.startswith("-"):
            raise ValueError(f"short argument: {short} should start with -")

        return short

    @validator("long")
    def long_should_start_with_double_dash(cls, long: str) -> str:
        """Checks if long argument had a double dash `--` before it.

        Args:
            long (str): Input long value

        Raises:
            ValueError: Raised if long doesn't have `--` before it

        Returns:
            str: Returns long if it's valid
        """
        if long and not long.startswith("--"):
            raise ValueError(f"long argument: {long} should start with --")

        return long
