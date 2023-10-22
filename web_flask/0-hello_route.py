#!/usr/bin/python3
"""This module starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index_page():
    """Displays Hello HBNB text of an index page"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
