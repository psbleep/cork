import os

from cork import DEPLOY_SCRIPT
from cork import create_deploy_script, create_executable

from tests import BASE_DIR, DEPLOY_SCRIPT_FILE, DEPLOY_SCRIPT_KWARGS


def test_create_deploy_script(setup_app_files):
    create_deploy_script(**DEPLOY_SCRIPT_KWARGS)
    with open(DEPLOY_SCRIPT_FILE) as f:
        deploy_script = f.read()
    assert deploy_script == DEPLOY_SCRIPT.format(**DEPLOY_SCRIPT_KWARGS)


def test_create_executable(setup_deploy_script, cleanup_deploy_script, setup_app_files):
    create_executable("example")
    assert os.path.exists(os.path.join(BASE_DIR, "dist"))
    assert os.path.exists(os.path.join(BASE_DIR, "dist/example_app"))
    assert os.path.exists(os.path.join(BASE_DIR, "dist/example_app/example_app"))
