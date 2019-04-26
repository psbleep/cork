# cork

Take a Flask web application and create a terminal application. "Inspired" by Electron.js.

Created during a silly/useless tech hackathon at [the Recurse Center](https://www.recurse.com/).

## Installation

`pip install cork`

## Usage

The `cork` package provides a command that will produce an executable. All you have to do is point it at a valid place to import a Flask app object.

If your Flask application lived in the file `example.py`, you could run this command:

`cork example`

PyInstaller runs under the hood to package up the dependencies and create the executable. Your executable will live in `dist/<example_>app/<example_>app`.

You can distribute this directory to any computer and it will execute your web application as a terminal interface, whether Python or any of your dependencies are installed or not.

## Distributing cork Apps

Right now cork apps require the Lynx console-based web browser to be installed on the host system. This requirement will be abolished in future releases. Other than that, a cork application executable should require no external dependencies (including any Python libraries, or even a Python interpreter).

## Future

PyInstaller creates very crowded directories. Because a Flask app may depend on templates or other files that are stored on the disk, I have not been able to find out a way to create a "true" one-file executable. A second-best option could be packaging all the PyInstaller cruft into a `deps` directory that is shipped with an app-launcher symlink that points to the executable file in `deps`.

cork apps depend on Lynx being installed on the host system. Short-term, cork should bundle a Lynx executable with the rest of the application dependencies so that the user does not need to install Lynx on their system. Longer-term, the web app should be browsed to in a more "headless" interface that hides the navigation features and enhances the illusion that the user is running a native terminal desktop application. There may be a way to approximate headless-Lynx in the way that Electron approximates headless-Chromium. Or we may need to write a pure-Python terminal web browser. This would also solve the problem of needing to bundle a Lynx binary, since PyInstaller could handle it like any Python dependency.
