import os
import shutil

import pytest

from click.testing import CliRunner

from tests import SOURCE, SOURCE_SPECFILE


DIRS = ["dist", "build", SOURCE]
FILES = ["corkfile", SOURCE_SPECFILE]


@pytest.fixture
def cleanup_corkfile(request):
    def cleanup():
        if os.path.exists("corkfile"):
            os.remove("corkfile")
    request.addfinalizer(cleanup)


@pytest.fixture
def create_corkfile(request):
    def cleanup():
        os.remove("corkfile")
    request.addfinalizer(cleanup)
    with open("corkfile", "w") as f:
        f.write("")


@pytest.fixture
def other_specfile(request):
    def cleanup():
        os.remove(".other.spec")
    request.addfinalizer(cleanup)
    with open(".other.spec", "w") as f:
        f.write("")


@pytest.fixture
def pyinstaller_files(request):
    def cleanup():
        for directory in DIRS:
            if os.path.exists(directory):
                shutil.rmtree(directory)
        for file_name in FILES:
            if os.path.exists(file_name):
                os.remove(file_name)
    request.addfinalizer(cleanup)
    for directory in DIRS:
        os.mkdir(directory)
    for file_name in FILES:
        with open(file_name, "w") as f:
            f.write("")


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_cork(mocker):
    mocker.patch("cork.create_corkfile")
    mocker.patch("cork.create_executable")
    mocker.patch("cork.bundle_dependencies")
    mocker.patch("cork.get_cleanup_list")
    mocker.patch("cork.cleanup_files")
