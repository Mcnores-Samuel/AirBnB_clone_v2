#!/usr/bin/python3
"""This module starts a Flask web application

Routes:
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ” followed by the value of the text
    variable (replace underscore _ symbols with a space )
"""
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


@app.route("/c/<text>", strict_slashes=False)
def process_text(text):
    """Applies text processing to the text form end user"""
    if text:
        text = text.replace("_", " ")
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
