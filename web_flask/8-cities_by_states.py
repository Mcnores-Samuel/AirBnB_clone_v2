#!/usr/bin/python3
"""starts a Flask web application"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """load all state object from the database"""
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def clear_session(exc):
    """closes a query session after a request"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
