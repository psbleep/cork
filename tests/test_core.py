import os
import pytest

import cork

from copy import copy

from tests import CORKFILE_KWARGS, SOURCE, SOURCE_SPECFILE


def test_corkfile_exists_after_create_corkfile(cleanup_corkfile):
    cork.create_corkfile(SOURCE, **CORKFILE_KWARGS)
    assert os.path.exists("corkfile")


def test_create_corkfile_does_not_overwrite_existing_corkfile(create_corkfile):
    with open("corkfile", "w") as f:
        f.write("")
    with pytest.raises(FileExistsError):
        cork.create_corkfile(SOURCE, **CORKFILE_KWARGS)


def test_create_corkfile_overwrite_existing_with_force_flag(create_corkfile):
    with open("corkfile", "w") as f:
        f.write("")
    corkfile_kwargs = copy(CORKFILE_KWARGS)
    corkfile_kwargs["force"] = True
    cork.create_corkfile(SOURCE, **corkfile_kwargs)
    with open("corkfile") as f:
        assert f.read() != ""


def test_corkfile_script_formatted_with_kwargs(cleanup_corkfile):
    cork.create_corkfile(SOURCE, **CORKFILE_KWARGS)
    with open("corkfile") as f:
        corkfile_script = f.read()
    corkfile_kwargs = copy(CORKFILE_KWARGS)
    del corkfile_kwargs["force"]
    for val in corkfile_kwargs.values():
        assert str(val) in corkfile_script


def test_create_executable_calls_formatted_pyinstaller_command(mocker):
    mocker.patch("os.system")
    cork.create_executable(SOURCE)
    os.system.assert_called_once_with(
        cork.PYINSTALLER_COMMAND.format(source=SOURCE)
    )


def test_bundle_dependencies_creates_bundle_directory(pyinstaller_files):
    cork.bundle_dependencies(SOURCE)
    assert os.path.exists("dist/bundle")


def test_bundle_dependencies_bundles_browser_binary(pyinstaller_files):
    cork.bundle_dependencies(SOURCE, browser="browsh", platform="linux")
    assert os.path.exists("dist/bundle/browsh")


def test_bundle_dependencies_source_does_not_exist():
    with pytest.raises(FileNotFoundError):
        cork.bundle_dependencies("invalid")


def test_get_cleanup_list_without_target_finds_files(pyinstaller_files):
    assert cork.get_cleanup_list(target=None) == [
        "build",
        SOURCE_SPECFILE,
        "corkfile",
    ]


def test_get_cleanup_list_with_target_does_not_include_other_files(
    pyinstaller_files,
    other_specfile
):
    with open(".other.spec", "w") as f:
        f.write("")
    cleanup_list = cork.get_cleanup_list(target=SOURCE)
    assert ".other.spec" not in cleanup_list


def test_get_cleanup_list_with_dist_flag(pyinstaller_files):
    cleanup_list = cork.get_cleanup_list(dist=True)
    assert "dist" in cleanup_list


def test_get_cleanup_list_target_does_not_exist():
    with pytest.raises(FileNotFoundError):
        cork.get_cleanup_list(target="invalid")


def test_cleanup_files_removes_listed_files(pyinstaller_files):
    cork.cleanup_files(["corkfile", SOURCE_SPECFILE])
    assert not os.path.exists("corkfile")
    assert not os.path.exists(SOURCE_SPECFILE)


def test_cleanup_files_removes_directories(pyinstaller_files):
    cork.cleanup_files(["dist", "build"])
    assert not os.path.exists("dist")
    assert not os.path.exists("build")


def test_cleanup_files_with_nonexisting_files(pyinstaller_files):
    cork.cleanup_files(["does_not_exist"])
    assert not os.path.exists("does_not_exist")


def test_get_platform():
    assert cork.get_platform("linux24323232") == "linux"
    assert cork.get_platform("openbsd823") == "openbsd"
    assert cork.get_platform("freebsd23828281") == "freebsd"
    assert cork.get_platform("darwin.1838.232.1.a") == "darwin"
