![screenshot.png](screenshot.png?raw=true "Cork Screenshot")
# Cork

Take a Flask web application and create a stand-alone terminal application. "Inspired" by Electron.js.

Created during a silly/useless tech hackathon at a place called the [the Recurse Center](https://www.recurse.com/). It is mostly my fault, but [@thechutrain](https://github.com/thechutrain) helped too.

Extreme alpha stages. I have only run this on a single computer (Linux with Python 3.7). Please do use it, but don't *use* it, you know?

## Installation

`pip install cork`

This is published in the official Python Packaging Index. Good jokes are about commitment. The package is very large because it packages binaries for every supported platform/browser combination with it.

## Quickstart

Cork is a utility that will produce a standalone executable from your Flask app. All you have to do is point it at a Python module with a valid `Flask` (app) object.

If your Flask application lived in a module called `example`, you could run this command:

`cork bundle example`

This will produce a `./dist` directory with an executable `./dist/example` and the application dependencies (static files, templates, etc) bundled into `./dist/bundle`. You can distribute the contents of the `./dist` directory to end users. The bundled dependencies directory will get moved out of the way when a user first runs the `./dist/example` executable.

To see the demo, you can run `cork bundle demo`.

## Commands

`cork bundle [source]`
Create an executable from the `source` module. Can be used with the following flags:

`-c, --cleanup` Remove the **corkfile** and PyInstaller artifacts after creating the executable.
`-f, --force` Overwrites any existing **corkfile**.
`-b, --browser` Set the terminal browser used to view the application. Defaults to `browsh`.
`-a, --app` Define the name of the Flask app object to be imported from the `source` module. Defaults to `app`.
`-p, --port` Set the default port to try launching the Flask app server on. Defaults to 5000. If the specified port is in use by another process, Cork applications increment by 1 until an open port is found.
`--teardown-route` Set the name of the special route that Cork application bind to the Flask app to allow for shutting down the Flask application server at quit time. Defaults to `teardown`.
`--teardown-function` Sets the name of the function that will decorated for the `--teardown-route` outlined above. Defaults to `teardown`.

`cork cleanup`
Remove artifacts left behind by the Cork and PyInstaller processes. By default, will delete th e corkfile and the PyInstaller `build` and any `.spec` files. The `dist` directory (with the Cork executable and dependency folder) is retained by default. Can be used with the following flags:

`-t, --target` Only remove `.spec` files associated with the specified cork application.
`-f, --force` Avoid confirmation prompt, go straight to deleting the files.
`-d, --dist` Delete the `dist` directory as well as the default files.

## How It Bundles

When running `cork bundle`:

* Cork creates a wrapper script for managing dependencies and running the application. This wrapper scrapped is called a **corkfile**.
* PyInstaller is called on this corkfile to create a single executable file out of this wrapper script.
* Non-Python file dependencies are collected into a single `bundle` directory and placed next to the executable PyInstaller created.

The main function of the corkfile script is to run a Flask application in a separate thread, then call a terminal browser to view it. A special teardown route is added to the Flask app so that when the user ends their browser session, the Flask application can be shut down instead of running until it is force-quit. The corkfile also handles the details of handling the file dependencies that cannot be placed into the executable itself.

PyInstaller packages up the Python interpereter and library dependencies into a single file executable. It places the executable in the `./dist` directory.

`cork` places your web app files and a copy of a terminal browser (defaults to [browsh](https://brow.sh)) into the `dist/bundle` directory. The web app files need to be shipped with the application so that static files, template files, etc are accessible on the target system. The browser is shipped so that the user does not need to have it already installed.

When the user first runs the application, this `bundle` folder of dependencies will get moved out of the way into the user's home config directory. If the `XDG_CONFIG_HOME` env variable is set, this value will be respected, otherwise it will default to `~HOME/.config`. All Cork applications installed on a system share the same browser binaries (stored in `~/.config/cork/browsers`). The web app files are stored in `~/.config/cork/<app_name>`, and that directory is added o the front of the system path so that Python looks there first for library imports.

A side-effect of this is that no two Cork applications can share a name on the same system, since there can only be one `~/.config/cork/<app_name>`. Cork applications will silently remove existing conflicting directories the first time they are run, and replace them with the dependencies they are shipped with.

## Development
Uses `pytest` for running the tests. After installing `requirements.txt` in your environment you should be able to run pytest from the root directory of this repo.

If I ever work on this in the future I would want to add support for other Python web app frameworks, especially [Django](https://www.djangoproject.com/), and other terminal-based browsers, especially [Lynx](https://lynx.browser.org/).

Pull requests and so on are encouraged. If you think this is fun/funny, go ahead and reach out!
