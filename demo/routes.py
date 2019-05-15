from flask import render_template
from demo import app


@app.route("/")
def index():
    return render_template("index.html", lang="jinja2")
