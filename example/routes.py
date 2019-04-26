from example import app
from flask import render_template


@app.route('/')
def index():
    kwargs = {
        "example_variable": "foo bar"
    }
    return render_template("index.html", **kwargs)
