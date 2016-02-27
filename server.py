"""Find your Spot!"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, send_from_directory, Response
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

    return render_template("index.html", professions=professions)


@app.route('/prueba')
def prueba():
    """Testing Jasny."""

    return render_template("rank.html")


@app.route('/search_states')
def search_states():
    """Search the top states with the info in the search form."""

    tax = request.args.get("tax")
    profession = request.args.get("profession")
    age = request.args.get("age")
    marital = request.args.get("marital")
    mstatus = marital + "_" + age
    wl = int(request.args.get("opcLiving"))
    wp = int(request.args.get("opcProfession"))
    wc = int(request.args.get("opcCrime"))
    wm = int(request.args.get("opcMarital"))
    professionptn = request.args.get("professionptn")
    top_states = ranking.get_top_states(tax, profession, mstatus, wl, wp, wc, wm, professionptn.strip())

    return jsonify(data=top_states)


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
    professionptn = request.args.get("professionptn")
    if (request.args.get("state_id")):
        state_id = request.args.get("state_id")
        top_counties = ranking.counties_by_id(state_id, tax, profession, mstatus, wl, wp, wc, wm, professionptn.strip())
    else:
        top_counties = ranking.get_top_counties(tax, profession, mstatus, wl, wp, wc, wm, professionptn.strip())
    return jsonify(data=top_counties)


@app.route('/map_counties')
def map_counties():
    """Show the map by counties"""

    return render_template("counties.html")


@app.route('/data/<path:path>')
def send_js(path):
    """Return an specific file from data directory."""

    return send_from_directory('data', path)


@app.route('/crime.json')
def crime_json():
    """ Generate the chart for Crime by State."""

    state_id = request.args.get("id")
    state = State.query.get(state_id)
    result = []
    result = [{"key": "Violent", "y": state.crime[0].violent_rate},
              {"key": "Murder", "y": state.crime[0].murder_rate},
              {"key": "Rape", "y": state.crime[0].rape_rate},
              {"key": "Assault", "y": state.crime[0].assault_rate},
              {"key": "Robery", "y": state.crime[0].robery_rate},
              {"key": "Property", "y": state.crime[0].property_rate},
              {"key": "Motor", "y": state.crime[0].motor_rate}]
    return jsonify(result=result)


@app.route('/marital.json')
def marital_json():
    """ Generate the chart for Marital by State."""

    state_id = request.args.get("id")

    query = """select m.state_id as id,
               (m.male_single_1524+m.male_single_2539+m.male_single_4059+m.male_single_60+
                m.female_single_1524+m.female_single_2539+m.female_single_4059+m.female_single_60) as totalsingle,
                (m.male_married_1524+m.male_married_2539+m.male_married_4059+m.male_married_60+
                m.female_married_1524+m.female_married_2539+m.female_married_4059+m.female_married_60) as totalmarried,
                (m.male_widowed_1524+m.male_widowed_2539+m.male_widowed_4059+m.male_widowed_60+
                m.female_widowed_1524+m.female_widowed_2539+m.female_widowed_4059+m.female_widowed_60) as totalwidowed,
                (m.male_divorced_1524+m.male_divorced_2539+m.male_divorced_4059+m.male_divorced_60+
                m.female_divorced_1524+m.female_divorced_2539+m.female_divorced_4059+m.female_divorced_60) as totaldivorced
                from statesmarital m
                where m.state_id = """+state_id+"""
                order by m.state_id"""

    maritalresult = db.session.execute(query).first()

    result = []
    result = [{"key": "Single", "y": maritalresult.totalsingle},
              {"key": "Married", "y": maritalresult.totalmarried},
              {"key": "Widowed", "y": maritalresult.totalwidowed},
              {"key": "Divorced", "y": maritalresult.totaldivorced}]
    return jsonify(result=result)


@app.route('/age.json')
def age_json():
    """ Generate the chart for Age by State."""

    state_id = request.args.get("id")

    query = """select m.state_id as id,
               (m.male_single_1524+m.male_married_1524+m.male_widowed_1524+m.male_divorced_1524+
                m.female_single_1524+m.female_married_1524+m.female_widowed_1524+m.female_divorced_1524) as total1524,
                (m.male_single_2539+m.male_married_2539+m.male_widowed_2539+m.male_divorced_2539+
                m.female_single_2539+m.female_married_2539+m.female_widowed_2539+m.female_divorced_2539) as total2539,
                (m.male_single_4059+m.male_married_4059+m.male_widowed_4059+m.male_divorced_4059+
                m.female_single_4059+m.female_married_4059+m.female_widowed_4059+m.female_divorced_4059) as total4059,
                (m.male_single_60+m.male_married_60+m.male_widowed_60+m.male_divorced_60+
                m.female_single_60+m.female_married_60+m.female_widowed_60+m.female_divorced_60) as total60
                from statesmarital m
                where m.state_id = """+state_id+"""
                order by m.state_id"""

    ageresult = db.session.execute(query).first()

    result = []
    result = [{"key": "15 - 24 yrs", "y": ageresult.total1524},
              {"key": "25 - 39 yrs", "y": ageresult.total2539},
              {"key": "40 - 59 yrs", "y": ageresult.total4059},
              {"key": "60 +", "y": ageresult.total60}]
    return jsonify(result=result)


@app.route('/chartsgral.json')
def chartsgral_json():
    """ Generate the charts for the given search."""

    tax = request.args.get("tax")
    chart = request.args.get("chart")
    profession = request.args.get("profession")
    age = request.args.get("age")
    marital = request.args.get("marital")
    mstatus = marital + "_" + age
    wl = int(request.args.get("opcLiving"))
    wp = int(request.args.get("opcProfession"))
    wc = int(request.args.get("opcCrime"))
    wm = int(request.args.get("opcMarital"))
    professionptn = request.args.get("professionptn")
    ntop = int(request.args.get("ntop"))
    top_states = ranking.top_chart_states(chart, tax, profession, mstatus, wl, wp, wc, wm, ntop, professionptn.strip())

    return jsonify(result=top_states)


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
