"""Utility file to calculate the rankings """

from sqlalchemy import func
from model import State, County
from model import StateProfession, StateLiving, CountyLiving, StateMarital
from model import CountyMarital, StateCrime, CountyCrime
from flask import session
import sys
from nvd3 import pieChart

from pandas import DataFrame
import pandas as pd

from model import connect_to_db, db
# from server import app


def get_top_counties(tax, profession, marital, wl, wp, wc, wm, professionptn='None'):
    """ Rank states and return a dictionary with all states"""

    query = """select co.state_id, co.county_id, co.name, sl.rank as livingrank,
               (cp.a_mean-cl.tax_"""+tax+""")as professionrank, cc.total as crimerank,
               (cm.male_"""+marital+""" + cm.female_"""+marital+""") as totalmarital
               from counties co
               left join countiesliving cl on (co.county_id = cl.county_id)
               left join statesliving sl on (co.state_id = sl.state_id)
               left join statesprofessions cp on (co.state_id = cp.state_id)
               left join statescrime cc on (co.state_id = cc.state_id)
               left join countiesmarital cm on (co.county_id =  cm.county_id)
               where cp.title = '"""+profession+"""'
               order by co.county_id"""


    result = db.session.execute(query)
    df1 = DataFrame(result.fetchall())
    df1.columns = result.keys()

    if (professionptn is not None):
        query = """select s.state_id, p.a_mean as professionptn
                   from statesprofessions p
                   left join states s on (s.state_id = p.state_id)
                   where p.title = '"""+professionptn+"""'"""
        result = db.session.execute(query)
        df2 = DataFrame(result.fetchall())
        df2.columns = result.keys()
        df = pd.merge(df1, df2,
                       left_on='state_id',
                       right_on='state_id')
    else:
        df = df1

    df = rank_dataframe(df, wl, wp, wc, wm)

    rank_counties = df.sort_index(by=['rankTotal'], ascending=False).fillna(0).to_dict('records')

    return rank_counties


def counties_by_id(state_id, tax):
    """Return all the counties of the given State"""

    query = """select co.name, co.percapita_income, co.median_household_income,
               co.population, co.number_households, cl.tax_"""+tax+""" as wage,
               (co.percapita_income - cl.tax_"""+tax+""") as discretionary_income
               from counties co
               left join countiesliving cl on (co.county_id = cl.county_id)
               where state_id = """ + state_id

    result = db.session.execute(query)
    counties = DataFrame(result.fetchall())
    counties.columns = result.keys()
    counties_by_state = counties.fillna(0).to_dict('records')
    return counties_by_state


def get_top_states(tax, profession, marital, wl, wp, wc, wm, professionptn='None'):
    """ Rank states and return a dictionary with all states"""


    query = """select s.state_id as id, s.name, 
               s.percapita_income, s.median_household_income, s.population, s.number_households,
               l.rank as livingrank,
               c.total as crimerank,
               (m.male_"""+marital+""" + m.female_"""+marital+""") as totalmarital,
               (p.a_mean-l.tax_"""+tax+""")as professionrank,
               p.a_mean, p.jobs_1000
               from states s
               left join statesliving l on (s.state_id = l.state_id)
               left join statesprofessions p on (s.state_id = p.state_id)
               left join statescrime c on (s.state_id = c.state_id)
               left join statesmarital m on (s.state_id =  m.state_id)
               where p.title = '"""+profession+"""'
               order by s.state_id"""

    result = db.session.execute(query)

    df1 = DataFrame(result.fetchall()).fillna(0)
    df1.columns = result.keys()

    if (professionptn != 'None'):
        query = """select s.state_id as id, p.a_mean as professionptn
                   from statesprofessions p
                   left join states s on (s.state_id = p.state_id)
                   where p.title = '"""+professionptn+"""'"""
        result = db.session.execute(query)
        df2 = DataFrame(result.fetchall())
        df2.columns = result.keys()
        df = pd.merge(df1, df2,
                       left_on='id',
                       right_on='id')
    else:
        df = df1

    df = rank_dataframe(df, wl, wp, wc, wm)

    rank_states = df.sort_index(by=['rate'], ascending=False).fillna(0).to_dict('records')

    return rank_states


def top_chart_states(chart, tax, profession, marital, wl, wp, wc, wm, ntop=3, professionptn='None'):
    """ Rank states and return a dictionary with all states"""

    query = """select s.state_id as id, s.name, l.rank as livingrank,
               c.total as crimerank,
               (m.male_"""+marital+""" + m.female_"""+marital+""") as totalmarital,
               (p.a_mean-l.tax_"""+tax+""")as professionrank
               from states s
               left join statesliving l on (s.state_id = l.state_id)
               left join statesprofessions p on (s.state_id = p.state_id)
               left join statescrime c on (s.state_id = c.state_id)
               left join statesmarital m on (s.state_id =  m.state_id)
               where p.title = '"""+profession+"""'
               order by s.state_id"""

    result = db.session.execute(query)
    df1 = DataFrame(result.fetchall())
    df1.columns = result.keys()

    if (professionptn != 'None'):
        query = """select s.state_id as id, p.a_mean as professionptn
                   from statesprofessions p
                   left join states s on (s.state_id = p.state_id)
                   where p.title = '"""+professionptn+"""'"""
        result = db.session.execute(query)
        df2 = DataFrame(result.fetchall())
        df2.columns = result.keys()
        df = pd.merge(df1, df2,
                       left_on='id',
                       right_on='id')
    else:
        df = df1

    df = rank_dataframe(df, wl, wp, wc, wm)

    rank_states = df.sort_index(by=['rate'], ascending=False).fillna(0).head(ntop)

    color = ["#F4442E", "#FC9E4F", "#EDD382", "#F2F3AE", "#A48DA7", "#B33F62", "#7B1E7A", "#49A078", "#9CC5A1", "#216869"]
    result = []
    i = 0
    for index, row in rank_states.iterrows():
        name = row['name']
        marital = row['totalmarital']
        living = row['livingrank']
        crimerank = row['crimerank']
        professionrank = row['professionrank']
        result.append({})

        if (chart=="marliv"):
            result[i] = {"key": name,
                         "color": color[i],
                         "values": [{"label": "Marital",
                                    "value": marital},
                                    {"label": "Living",
                                    "value": living}
                                    ]}
        else:
            result[i] = {"key": name,
                         "color": color[i],
                         "values": [{"label": "Crime",
                                    "value": crimerank},
                                    {"label": "Profession",
                                    "value": professionrank}
                                    ]}                    
        i += 1
    return result


def rank_dataframe(df, wl, wp, wc, wm):
    """Calculate the rank and return a dataframe"""

    df[['totalmarital', 'professionrank', 'crimerank']].astype(float).fillna(0)
    if ('professionptn' in df):
        df['personalprofession'] = df['professionrank']
        df['professionrank'] = df['personalprofession'] + df['professionptn']
    else:
        df['personalprofession'] = df['professionrank']
        df['professionptn'] = 'NA'
    df['LivRank'] = (df['livingrank'].rank(ascending=False)) * wl
    df['profRank'] = df['professionrank'].rank(ascending=True) * wp
    df['criRank'] = df['crimerank'].rank(ascending=False) * wc
    df['marRank'] = df['totalmarital'].rank(ascending=True) * wm
    df['Total'] = (df['LivRank']) + (df['profRank']) + (df['criRank']) + (df['marRank'])
    df['rate'] = df['Total'].rank(ascending=True)

    df['totalmarital'] = df['totalmarital'].map('{:.2f}'.format)
    df['professionrank'] = df['professionrank'].map('{:.2f}'.format)
    df.to_csv('rankdataframe.csv')

    return df

# if __name__ == "__main__":
#     # connect_to_db(app)
