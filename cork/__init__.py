import os
import shutil


DEPLOY_SCRIPT = """import threading
import webbrowser

import requests

from flask import request

from {app_source} import {app_name}


@app.route("/{teardown_route}")
def {teardown_function_name}():
    teardown_function = request.environ.get("werkzeug.server.shutdown")
    teardown_function()
    return "Application shutdown."


if __name__ == "__main__":
    flask_thread = threading.Thread(target={app_name}.run)
    flask_thread.start()
    browser = webbrowser.get('{browser}')
    browser.open("http://localhost:{port}")
    requests.get("http://localhost:{port}/{teardown_route}")
    flask_thread.join()
"""


def create_deploy_script(
    app_source="cork_app",
    app_name="app",
    teardown_route="teardown",
    teardown_function_name="teardown",
    browser="lynx",
    port=5000
):
    script_name = "{}_app.py".format(app_source)
    deploy_script = DEPLOY_SCRIPT.format(
        app_source=app_source,
        app_name=app_name,
        teardown_route=teardown_route,
        teardown_function_name=teardown_function_name,
        browser=browser,
        port=port
    )
    with open(script_name, "w") as f:
        f.write(deploy_script)


PYINSTALLER_COMMAND = "pyinstaller --clean --add-data {app_source}:./{app_source} {app_source}_app.py"


def create_executable(app_source):
    os.system(PYINSTALLER_COMMAND.format(app_source=app_source))
    base_dir = os.getcwd()
    dist_dir = os.path.join(base_dir, "dist")
    app_files = os.path.join(dist_dir, "{}_app".format(app_source))
    deps_dir = os.path.join(dist_dir, "deps")
    executable = os.path.join(deps_dir, "{}_app".format(app_source))
    launcher = os.path.join(dist_dir, app_source)
    shutil.move(app_files, deps_dir)
    os.symlink(executable, launcher)
