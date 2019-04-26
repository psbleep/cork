import os
import shutil

import pytest

from cork import DEPLOY_SCRIPT

from tests import (
    DEPLOY_SCRIPT_FILE, DEPLOY_SCRIPT_KWARGS,
    EXAMPLE_APP_DIR, DIST, BUILD, SPEC
)


@pytest.fixture
def setup_app_files(request):
    def cleanup():
        for directory in [EXAMPLE_APP_DIR, DIST, BUILD]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
        if os.path.exists(SPEC):
            os.remove(SPEC)
    if os.path.exists(EXAMPLE_APP_DIR):
        shutil.rmtree(EXAMPLE_APP_DIR)
    os.mkdir(EXAMPLE_APP_DIR)
    request.addfinalizer(cleanup)


@pytest.fixture
def cleanup_deploy_script(request):
    def cleanup():
        if os.path.exists(DEPLOY_SCRIPT_FILE):
            os.remove(DEPLOY_SCRIPT_FILE)
    request.addfinalizer(cleanup)


@pytest.fixture
def setup_deploy_script():
    with open(DEPLOY_SCRIPT_FILE, "w") as f:
        f.write(DEPLOY_SCRIPT.format(**DEPLOY_SCRIPT_KWARGS))


@pytest.fixture
def mock_cork(mocker):
    mocker.patch("cork.create_deploy_script")
    mocker.patch("cork.create_executable")
