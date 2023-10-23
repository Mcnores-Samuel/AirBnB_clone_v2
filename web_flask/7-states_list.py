#!/usr/bin/python3
"""Starts a flask web server"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Queries all objects in the states table from the
    database to the html page
    """
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def clear_session(exc):
    """Teardown the session object when the request has been processed"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
