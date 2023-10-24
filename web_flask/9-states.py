#!/usr/bin/python3
"""Starts a flask web server"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states_list():
    """Queries all objects in the states table from the
    database to the html page
    """
    states = storage.all("State")
    return render_template('9-states.html', states=states)


@app.route("/states/<string:id>", strict_slashes=False)
def cities_by_states(id):
    """load all state object from the database"""
    state = storage.all("State")
    if "State." + id in state:
        state = state["State." + id]
        return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def clear_session(exc):
    """Teardown the session object when the request has been processed"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
