#!/usr/bin/python3
"""This module starts a Flask web application

Routes:
  /: display “Hello HBNB!”
 /hbnb: display “HBNB”
 /c/<text>: display “C ”, followed by the value of the text
    variable (replace underscore _ symbols with a space )
 /python/<text>: display “Python ”, followed by the value of
    the text variable (replace underscore _ symbols with a space )
"""
from flask import Flask
from flask import render_template

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


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def process_text2(text="is cool"):
    """Applies text processing to the text form end user"""
    if text:
        text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def number_processing(n):
    """Checks if n post data is a number"""
    return '{} is a number'.format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Renders a template html if n is an integer"""
    return render_template('5-number.html', number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """Renders a template html if n is an integer
    and the template displays a number on either is odd or even.
    """
    return render_template('6-number_odd_or_even.html', number=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
