"""RP To-Do entry point script."""

# cmds/__main__.py

from cmds import __app_name__
from cmds.views import cli


def main() -> None:
    """Starting point of CLI application"""
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
