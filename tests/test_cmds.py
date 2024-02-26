# Integration tests

import pytest
from typer.testing import CliRunner

from cmds import __app_name__, __version__
from cmds.views import cli

runner = CliRunner()


@pytest.mark.integration
class TestCmds:
    def test_version(self):
        result = runner.invoke(cli.app, ["--version"])
        assert result.exit_code == 0
        assert f"{__app_name__} v{__version__}\n" in result.stdout
