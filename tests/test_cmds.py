# Integration tests

import pytest
from typer.testing import CliRunner

from cmds.models.constants import APP_NAME, VERSION
from cmds.views import cli

runner = CliRunner()


@pytest.mark.integration
class TestCmds:
    def test_version(self):
        result = runner.invoke(cli.app, ["--version"])
        assert result.exit_code == 0
        assert f"{APP_NAME} v{VERSION}\n" in result.stdout
