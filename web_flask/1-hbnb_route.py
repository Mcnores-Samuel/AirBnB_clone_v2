#!/usr/bin/python3
"""This module starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index_page():
    """Displays Hello HBNB text of an index page"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays HBNB text to the redirected path"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
