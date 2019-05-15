import os
import shutil


CORKFILE_SCRIPT = """import os
import socket
import shutil
import sys
import threading

import requests

from flask import request

CONFIG_DIR = os.environ.get(
    "XDG_CONFIG_HOME",
    os.path.join(os.path.expanduser("~"), ".config")
)

CORK_DIR = os.path.join(CONFIG_DIR, "cork")
BROWSERS_DIR = os.path.join(CORK_DIR, "browsers")
if not os.path.exists(CORK_DIR):
    os.mkdir(CORK_DIR)
    os.mkdir(BROWSERS_DIR)

BROWSER_BIN = os.path.join(BROWSERS_DIR, "{browser}")
APP_DIR = os.path.join(CORK_DIR, "{source}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLE_DIR = os.path.join(BASE_DIR, "bundle")

if not os.path.exists(BUNDLE_DIR) and not os.path.exists(APP_DIR):
    raise FileNotFoundError(
        "Cork could not find the dependencies bundled with this application! "
        "Try redownloading this application (with the included 'bundle' "
        "directory) and running again."
    )

if os.path.exists(BUNDLE_DIR):
    if not os.path.exists(BROWSER_BIN):
        os.rename(os.path.join(BUNDLE_DIR, "{browser}"), BROWSER_BIN)
    else:
        bundled_browser_bin = os.path.join(BUNDLE_DIR, "{browser}")
        if os.path.exists(bundled_browser_bin):
            os.remove(bundled_browser_bin)
    if os.path.exists(APP_DIR):
        shutil.rmtree(APP_DIR)
    os.rename(BUNDLE_DIR, APP_DIR)
sys.path.insert(0, APP_DIR)


from {source} import {app}

{app}.root_path = APP_DIR


@app.route("/{teardown_route}")
def {teardown_function}():
    func = request.environ.get("werkzeug.server.shutdown")
    func()
    return "Application shutdown."


port = {starting_port}
port_open = False
while not port_open:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        port_open = not sock.connect_ex(("localhost", port)) == 0
    if not port_open:
        port += 1
url_port = str(port)


if __name__ == "__main__":
    flask_thread = threading.Thread(target={app}.run, kwargs={{"port": port}})
    flask_thread.start()
    os.system(BROWSER_BIN + " http://localhost:" + url_port)
    requests.get("http://localhost:" + url_port + "/{teardown_route}")
    flask_thread.join()
"""

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_corkfile(source, force=False, **kwargs):
    if not force and os.path.exists("corkfile"):
        raise FileExistsError(
            "Corkfile already exists in this directory!"
        )
    corkfile_script = CORKFILE_SCRIPT.format(source=source, **kwargs)
    with open("corkfile", "w") as f:
        f.write(corkfile_script)


PYINSTALLER_COMMAND = (
    "pyinstaller --onefile --noupx --windowed --clean "
    "corkfile --name {source}"
)


def create_executable(source):
    os.system(PYINSTALLER_COMMAND.format(source=source))


def bundle_dependencies(source, browser="browsh", platform="linux"):
    if not os.path.exists(source):
        raise FileNotFoundError(
            "App source not found: {}".format(source)
        )
    dist_dir = os.path.join(os.getcwd(), "dist")
    bundle_dir = os.path.join(dist_dir, "bundle")
    shutil.copytree(source, bundle_dir)
    browser_dir = os.path.join(PACKAGE_DIR, "browsers")
    browser_bin = os.path.join(browser_dir, "{}_{}".format(browser, platform))
    shutil.copy(browser_bin, os.path.join(bundle_dir, browser))


def get_cleanup_list(target=None, dist=False):
    cleanup_list = []
    if target and not os.path.exists(target):
        raise FileNotFoundError(
            "Target not found: {}.".format(target)
        )
    if os.path.exists("build"):
        cleanup_list.append("build")
    if dist and os.path.exists("dist"):
        cleanup_list.append("dist")
    base_dir = os.getcwd()
    if not target:
        cork_and_spec_files = [f for f in os.listdir(base_dir)
                               if f.endswith(".spec") or f == "corkfile"]
    else:
        cork_and_spec_files = ["{}.spec".format(target),
                               "corkfile"]
    cleanup_list.extend(cork_and_spec_files)
    return cleanup_list


def cleanup_files(cleanup_files):
    for file_name in cleanup_files:
        if not os.path.exists(file_name):
            continue
        elif os.path.isdir(file_name):
            shutil.rmtree(file_name)
        else:
            os.remove(file_name)


def get_platform(platform):
    for system in ["linux", "openbsd", "freebsd", "darwin", "windows"]:
        if platform.startswith(system):
            return system
