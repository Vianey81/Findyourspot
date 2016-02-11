"""Utility file to calculate the rankings """

from sqlalchemy import func
from model import State, County, StatePopulation, CountyPopulation
from model import StateProfession, StateLiving, CountyLiving, StateMarital
from model import CountyMarital, StateCrime, CountyCrime

from pandas import DataFrame

from model import connect_to_db, db
from server import app


def get_top_states(tax, profession, marital, wl, wp, wc, wm):
    query = """select s.state_id, s.name, l.rank as livingrank,
               (p.a_mean-l.tax_"""+tax+""")as professionrank, c.total as crimerank,
               (m.male_"""+marital+""" + m.female_"""+marital+""") as totalmarital
               from states s
               left join statesliving l on (s.state_id = l.state_id)
               left join statesprofessions p on (s.state_id = p.state_id)
               left join statescrime c on (s.state_id = c.state_id)
               left join statesmarital m on (s.state_id =  m.state_id)
               where p.title = '"""+profession+"""'
               order by s.state_id"""

    result = db.session.execute(query)
    df = DataFrame(result.fetchall())
    df.columns = result.keys()

    df['LivRank'] = (df['livingrank'].rank(ascending=False)) * wl
    df['profRank'] = df['professionrank'].rank(ascending=True) * wp
    df['criRank'] = df['crimerank'].rank(ascending=True) * wc
    df['marRank'] = df['totalmarital'].rank(ascending=True) * wm
    df['rankTotal'] = (df['LivRank']) + (df['profRank']) + (df['criRank']) + (df['marRank'])

    rank_states = df.sort_index(by=['rankTotal'], ascending=False).fillna(0).to_dict('records')
    print "Living:",wl, " Prof: ", wp, " Crime: ", wc," Marital: ", wm
    return rank_states


if __name__ == "__main__":
    connect_to_db(app)
