#!/usr/bin/python3
""" Starts a Flask web application listening on port 5000
with four routes and using templates

Routes:
    - /hbnb_filters: display a HTML page
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)

@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ Display a HTML page
    H1 tag: States
    UL tag: list of all State objects present in DBStorage
    LI tag: description of one State: <state.id>: <B><state.name></B>
    H2 tag: Cities
    UL tag: list of City objects linked to the State
    """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)

@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')