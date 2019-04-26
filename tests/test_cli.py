from click.testing import CliRunner

import cork
from cork.__main__ import run_cork


def test_run_cork(mock_cork):
    runner = CliRunner()
    runner.invoke(run_cork, "example_app")
    cork.create_deploy_script.assert_called_once_with("example_app")
    cork.create_executable.assert_called_once_with("example_app")


def test_run_cork_trims_trailing_slash(mock_cork):
    runner = CliRunner()
    runner.invoke(run_cork, "example_app/")
    cork.create_deploy_script.assert_called_once_with("example_app")
    cork.create_executable.assert_called_once_with("example_app")
