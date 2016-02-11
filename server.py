"""Find your Spot!"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import func
from model import connect_to_db, db
from model import State, County, StatePopulation, CountyPopulation
from model import StateProfession, StateLiving, CountyLiving, StateMarital
from model import CountyMarital, StateCrime, CountyCrime
import ranking
from flask import jsonify
import json


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "CRAYOLA"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    professions = db.session.query(StateProfession.title).filter_by(level='major').group_by(StateProfession.title).all()

    return render_template("homepage.html", professions=professions)


@app.route('/search_states')
def search_states():
    """Search the top states"""

    tax = request.args.get("tax")
    profession = request.args.get("profession")
    age = request.args.get("age")
    marital = request.args.get("marital")
    mstatus = marital + "_" + age
    wl = int(request.args.get("opcLiving"))
    wp = int(request.args.get("opcProfession"))
    wc = int(request.args.get("opcCrime"))
    wm = int(request.args.get("opcMarital"))
    top_states = ranking.get_top_states(tax, profession, mstatus, wl, wp, wc, wm)

    return render_template("rank.html", result=top_states)


@app.route('/search_counties')
def search_counties():
    """Search the top counties"""

    tax = request.args.get("tax")
    profession = request.args.get("profession")
    age = request.args.get("age")
    marital = request.args.get("marital")
    mstatus = marital + "_" + age
    wl = int(request.args.get("opcLiving"))
    wp = int(request.args.get("opcProfession"))
    wc = int(request.args.get("opcCrime"))
    wm = int(request.args.get("opcMarital"))
    top_counties = ranking.get_top_counties(tax, profession, mstatus, wl, wp, wc, wm)
    return render_template("rank.html", result=top_counties)


@app.route('/map_counties')
def map_counties():
    """Show the map by counties"""

    return render_template("counties.html")


@app.route('/data/<path:path>')
def send_js(path):
    """Return an specific file from data directory."""

    return send_from_directory('data', path)


@app.route('/map_states')
def map_states():
    """Show the map by States"""

    return render_template("states.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
