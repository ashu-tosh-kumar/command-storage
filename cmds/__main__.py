"""Cmds entry point script."""

from cmds import __app_name__
from cmds.views._create_cli import *  # noqa: F401 # NOSONAR
from cmds.views._delete_cli import *  # noqa: F401 # NOSONAR
from cmds.views._read_cli import *  # noqa: F401 # NOSONAR
from cmds.views._update_cli import *  # noqa: F401 # NOSONAR
from cmds.views.cli import app


def main() -> None:
    """Starting point of CLI application"""
    app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
