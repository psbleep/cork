from click.testing import CliRunner

import cork
from cork.__main__ import run_cork


def test_run_cork(mocker):
    mocker.patch("cork.create_deploy_script")
    mocker.patch("cork.create_executable")
    runner = CliRunner()
    runner.invoke(run_cork, "example_app")
    cork.create_deploy_script.assert_called_once_with("example_app")
    cork.create_executable.assert_called_once_with("example_app")
