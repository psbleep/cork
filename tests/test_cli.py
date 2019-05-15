import cork

from copy import copy

from cork.__main__ import cli

from tests import CORKFILE_KWARGS


def test_cli_bundle_calls_cork_commands(runner, mock_cork):
    runner.invoke(cli, ["bundle", "source"])
    cork.create_corkfile.assert_called_once_with(
        source="source",
        **CORKFILE_KWARGS
    )
    cork.create_executable.assert_called_once_with("source")
    cork.bundle_dependencies.assert_called_once_with(
        "source",
        browser="browsh",
        platform="linux",
    )


def test_cli_bundle_options_changes_corkfile_formatting(runner, mock_cork):
    runner.invoke(cli, ["bundle", "source", "--port", "3000"])
    corkfile_options = copy(CORKFILE_KWARGS)
    corkfile_options["starting_port"] = 3000
    cork.create_corkfile.assert_called_once_with(
        source="source",
        **corkfile_options
    )


def test_cli_bundle_does_not_call_cleanup_by_default(runner, mock_cork):
    runner.invoke(cli, ["bundle", "source"])
    cork.get_cleanup_list.assert_not_called()
    cork.cleanup_files.assert_not_called()


def test_cli_bundle_does_call_cleanup_when_called(runner, mock_cork):
    runner.invoke(cli, ["bundle", "source", "--cleanup"])
    cork.get_cleanup_list.assert_called_once_with(target="source", dist=False)
    cork.cleanup_files.assert_called_once()


def test_cli_cleanup_with_force_flag(runner, mock_cork):
    runner.invoke(cli, ["cleanup", "--force"])
    cork.cleanup_files.assert_called_once()


def test_cli_cleanup_confirms_without_force_flag(runner, mock_cork):
    runner.invoke(cli, ["cleanup"], input="n\n")
    cork.cleanup_files.assert_not_called()


def test_cli_cleanup_confirmation_without_force_flag(runner, mock_cork):
    runner.invoke(cli, ["cleanup"], input="y\n")
    cork.cleanup_files.assert_called_once()


def test_cli_cleanup_called_with_dist_flag(runner, mock_cork):
    runner.invoke(cli, ["cleanup", "--force", "--dist"])
    cork.get_cleanup_list.assert_called_once_with(target=None, dist=True)
    cork.cleanup_files.assert_called_once()
