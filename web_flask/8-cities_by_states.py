#!/usr/bin/python3
"""starts a Flask web application"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states_list():
    """Queries all objects in the states table from the
    database to the html page
    """
    states = storage.all("State")
    return render_template('9-states.html', states=states)


@app.route("/states/<string:id>", strict_slashes=False)
def cities_by_states():
    """load all state object from the database"""
    states = storage.all("State")
    return render_template("9-states.html", city_by_state=states)


@app.teardown_appcontext
def clear_session(exc):
    """closes a query session after a request"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
