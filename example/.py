import threading
import webbrowser

import requests

from flask import request

from example/ import app


@app.route("/teardown")
def teardown():
    teardown_function = request.environ.get("werkzeug.server.shutdown")
    teardown_function()
    return "Application shutdown."


if __name__ == "__main__":
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()
    browser = webbrowser.get(lynx)
    browser.open("http://localhost:5010")
    requests.get("http://localhost:5010/teardown")
    flask_thread.join()
