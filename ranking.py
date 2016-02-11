"""Utility file to calculate the rankings """

from sqlalchemy import func
from model import State, County, StatePopulation, CountyPopulation
from model import StateProfession, StateLiving, CountyLiving, StateMarital
from model import CountyMarital, StateCrime, CountyCrime

from pandas import DataFrame

from model import connect_to_db, db
from server import app


def get_top_counties(tax, profession, marital, wl, wp, wc, wm):
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
    df = DataFrame(result.fetchall())
    df.columns = result.keys()

    df['LivRank'] = (df['livingrank'].rank(ascending=False)) * wl
    df['profRank'] = df['professionrank'].rank(ascending=True) * wp
    df['criRank'] = df['crimerank'].rank(ascending=True) * wc
    df['marRank'] = df['totalmarital'].rank(ascending=True) * wm
    df['Total'] = (df['LivRank']) + (df['profRank']) + (df['criRank']) + (df['marRank'])
    df['rankTotal'] = df['Total'].rank(ascending=True)

    rank_counties = df.sort_index(by=['rankTotal'], ascending=False).fillna(0).to_dict('records')
    create_tsv(df.fillna(0), ["county_id", "rankTotal"])
    print "Living:", wl, " Prof: ", wp, " Crime: ", wc, " Marital: ", wm
    return rank_counties


def get_top_states(tax, profession, marital, wl, wp, wc, wm):
    """ Rank states and return a dictionary with all states"""

    query = """select s.state_id as id, s.name, l.rank as livingrank,
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
    df['Total'] = (df['LivRank']) + (df['profRank']) + (df['criRank']) + (df['marRank'])
    df['rate'] = df['Total'].rank(ascending=True)

    rank_states = df.sort_index(by=['rate'], ascending=False).fillna(0).to_dict('records')
    create_tsv(df.fillna(0), ["id", "rate"])
    print "Living:", wl, " Prof: ", wp, " Crime: ", wc, " Marital: ", wm
    return rank_states


def create_tsv(df, header):
    """ Create file tsv to with the results"""

    df.to_csv('data/rankresults.tsv', mode='a', sep='\t', index=False,  columns=header)
    return None


if __name__ == "__main__":
    connect_to_db(app)
