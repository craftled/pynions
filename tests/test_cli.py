import os
from click.testing import CliRunner
from pynions.cli import cli


def test_new_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["new", "testproject"])
        assert result.exit_code == 0
        assert os.path.exists("testproject")
        assert os.path.exists("testproject/workflows")
        assert os.path.exists("testproject/.env.example")
        assert os.path.exists("testproject/requirements.txt")
