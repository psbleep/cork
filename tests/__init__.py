import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
EXAMPLE_APP_DIR = os.path.join(BASE_DIR, "example_app")
DIST = os.path.join(BASE_DIR, "dist")
BUILD = os.path.join(BASE_DIR, "build")
SPEC = os.path.join(BASE_DIR, "example_app.spec")
DEPLOY_SCRIPT_FILE = os.path.join(BASE_DIR, "example_app.py")
DEPLOY_SCRIPT_KWARGS = dict(
    app_source="example",
    app_name="app",
    teardown_route="teardown",
    teardown_function_name="teardown",
    browser="lynx",
    port=5010
)
