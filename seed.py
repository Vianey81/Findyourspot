"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import State, County, StatePopulation, CountyPopulation
from model import StateProfession, StateLiving, CountyLiving, StateMarital
from model import CountyMarital, StateCrime, CountyCrime
# from dateutil import parser
import datetime

from model import connect_to_db, db
from server import app

import pandas as pd
import numpy as np


def load_states():
    """Load states from  into database."""

    print "States"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    State.query.delete()

    # Read identifiers.csv file and insert data
    df = pd.read_csv('data/identifiers.csv')
    print(df.columns)
    states = df.groupby("sh_state").first()

    for index, row in states.iterrows():
        sh_state = row[0]
        name = row[2]
        id_state = row[3]
        longitude = row[5]
        latitude = row[6]

        state = State(state_id=id_state,
                      name=name,
                      short_name=sh_state,
                      longitude=longitude,
                      latitude=latitude)

        print sh_state, "-", name, "-", id_state, longitude, latitude
        print state

        # We need to add to the session or it won't ever be stored
        db.session.add(state)

    # Once we're done, we should commit our work
    db.session.commit()


def load_counties():
    """Load counties from  into database."""

    print "Counties"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    County.query.delete()

    # Read identifiers.csv file and insert data
    df = pd.read_csv('data/identifiers.csv')
    print(df.columns)

    for index, row in df.iterrows():
        name = row[2]
        id_state = row[4]
        id_county = row[5]
        longitude = row[6]
        latitude = row[7]

        county = County(county_id=id_county,
                        name=name,
                        state_id=id_state,
                        longitude=longitude,
                        latitude=latitude)

        print id_state, "-", name, "-", id_county, longitude, latitude

        # We need to add to the session or it won't ever be stored
        db.session.add(county)

    # Once we're done, we should commit our work
    db.session.commit()


def load_professions():
    """Load professions from  into database."""

    print "Professions"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    StateProfession.query.delete()

    # Read professions.csv file and insert data
    df = pd.read_csv('data/professions.csv')
    print(df.columns)

    for index, row in df.iterrows():
        name = row[4]
        id_state = row[0]
        if (row[11] == '*') or (row[11] == '#'):
            a_mean = 0
        else:
            a_mean = float(row[11].replace(',', ''))
        level = row[5]
        if (row[8] == '**'):
            jobs_1000 = 0
        else:
            jobs_1000 = row[8]

        stateprofession = StateProfession(state_id=id_state,
                                          title=name,
                                          a_mean=a_mean,
                                          level=level,
                                          jobs_1000=jobs_1000)

        print id_state, "-", name, "-", a_mean, level, jobs_1000

        # We need to add to the session or it won't ever be stored
        db.session.add(stateprofession)

    # Once we're done, we should commit our work
    db.session.commit()


def load_crimestate():
    """Load crime by state from  into database."""

    print "Crime"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    StateCrime.query.delete()

    # Read crimedate.csv file and insert data
    # Crime is only by state
    df = pd.read_csv('data/crimedata.csv')
    print(df.columns)

    for index, row in df.iterrows():
        name = row[0]
        state = State.query.filter(State.name.like(name)).first()
        if state:
            state_id = state.state_id
        else:
            print "Error. State not found!"
        violent_rate = row[11]
        murder_rate = row[12]
        rape_rate = row[13]
        assault_rate = row[15]
        robery_rate = row[14]
        property_rate = row[16]
        motor_rate = row[19]
        total = sum(row[11:17]) + row[19]

        statecrime = StateCrime(state_id=state_id,
                                violent_rate=violent_rate,
                                murder_rate=murder_rate,
                                rape_rate=rape_rate,
                                assault_rate=assault_rate,
                                robery_rate=robery_rate,
                                property_rate=property_rate,
                                motor_rate=motor_rate,
                                total=total)

        print state_id, "-", name, "-", violent_rate, murder_rate

        # We need to add to the session or it won't ever be stored
        db.session.add(statecrime)

    # Once we're done, we should commit our work
    db.session.commit()


def load_maritalcounties():
    """Load marital status from  into database."""

    print "Marital Status"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    CountyMarital.query.delete()

    # Read maritalstatus.csv file and insert data
    df = pd.read_csv('data/maritalstatus.csv')
    print(df.columns)

    # All data is transform to percentage
    for index, row in df.iterrows():
        county_id = row[0]
        total = float(row[2])
        total_male = (float(row[3]) * 100) / total
        total_female = (float(row[96]) * 100) / total
        male_single_1524 = (sum(row[5:8]) * 100) / total
        male_single_2539 = (sum(row[8:11]) * 100) / total
        male_single_4059 = (sum(row[11:15]) * 100) / total
        male_single_60 = (sum(row[15:18]) * 100) / total
        male_married_1524 = ((sum(row[37:40]) + sum(row[21:24])) * 100) / total
        male_married_2539 = ((sum(row[40:43]) + sum(row[24:27])) * 100) / total
        male_married_4059 = ((sum(row[43:47]) + sum(row[27:31])) * 100) / total
        male_married_60 = ((sum(row[47:51]) + sum(row[31:35])) * 100) / total
        male_widowed_1524 = (sum(row[67:70]) * 100) / total
        male_widowed_2539 = (sum(row[70:73]) * 100) / total
        male_widowed_4059 = (sum(row[73:77]) * 100) / total
        male_widowed_60 = (sum(row[77:81]) * 100) / total
        male_divorced_1524 = ((sum(row[52:55]) + sum(row[82:85])) * 100) / total
        male_divorced_2539 = ((sum(row[55:58]) + sum(row[85:88])) * 100) / total
        male_divorced_4059 = ((sum(row[58:62]) + sum(row[88:92])) * 100) / total
        male_divorced_60 = ((sum(row[62:66]) + sum(row[92:95])) * 100) / total

        female_single_1524 = (sum(row[98:101]) * 100) / total
        female_single_2539 = (sum(row[101:104]) * 100) / total
        female_single_4059 = (sum(row[104:108]) * 100) / total
        female_single_60 = (sum(row[108:112]) * 100) / total
        female_married_1524 = ((sum(row[114:117]) + sum(row[130:133])) * 100) / total
        female_married_2539 = ((sum(row[117:120]) + sum(row[133:136])) * 100) / total
        female_married_4059 = ((sum(row[120:124]) + sum(row[136:140])) * 100) / total
        female_married_60 = ((sum(row[124:128]) + sum(row[140:143])) * 100) / total
        female_widowed_1524 = (sum(row[160:163]) * 100) / total
        female_widowed_2539 = (sum(row[163:166]) * 100) / total
        female_widowed_4059 = (sum(row[166:170]) * 100) / total
        female_widowed_60 = (sum(row[170:174]) * 100) / total
        female_divorced_1524 = ((sum(row[145:148]) + sum(row[175:178])) * 100) / total
        female_divorced_2539 = ((sum(row[148:151]) + sum(row[178:181])) * 100) / total
        female_divorced_4059 = ((sum(row[151:155]) + sum(row[181:185])) * 100) / total
        female_divorced_60 = ((sum(row[155:159]) + sum(row[185:188])) * 100) / total

        county_marital = CountyMarital(county_id=county_id,
                                      total_male=total_male,
                                      total_female=total_female,
                                      male_single_1524=male_single_1524,
                                      male_single_2539=male_single_2539,
                                      male_single_4059=male_single_4059,
                                      male_single_60=male_single_60,
                                      male_married_1524=male_married_1524,
                                      male_married_2539=male_married_2539,
                                      male_married_4059=male_married_4059,
                                      male_married_60=male_married_60,
                                      male_widowed_1524=male_widowed_1524,
                                      male_widowed_2539=male_widowed_2539,
                                      male_widowed_4059=male_widowed_4059,
                                      male_widowed_60=male_widowed_60,
                                      male_divorced_1524=male_divorced_1524,
                                      male_divorced_2539=male_divorced_2539,
                                      male_divorced_4059=male_divorced_4059,
                                      male_divorced_60=male_divorced_60,
                                      female_single_1524=female_single_1524,
                                      female_single_2539=female_single_2539,
                                      female_single_4059=female_single_4059,
                                      female_single_60=female_single_60,
                                      female_married_1524=female_married_1524,
                                      female_married_2539=female_married_2539,
                                      female_married_4059=female_married_4059,
                                      female_married_60=female_married_60,
                                      female_widowed_1524=female_widowed_1524,
                                      female_widowed_2539=female_widowed_2539,
                                      female_widowed_4059=female_widowed_4059,
                                      female_widowed_60=female_widowed_60,
                                      female_divorced_1524=female_divorced_1524,
                                      female_divorced_2539=female_divorced_2539,
                                      female_divorced_4059=female_divorced_4059,
                                      female_divorced_60=female_divorced_60)

        print county_id, "-", total, "-", total_male, total_female

        # We need to add to the session or it won't ever be stored
        db.session.add(county_marital)

    # Once we're done, we should commit our work
    db.session.commit()


def load_countiesliving(afile):

    # CountyLiving.query.delete()
    df = pd.DataFrame(pd.read_csv(afile).values.reshape(-1, 8))
    print df

    for index, row in df.iterrows():
        county_id = row[0].split('/')[-1]
        wage_1ad = row[1] * 2080
        wage_2ad = row[2] * 2080
        wage_22 = row[3] * 2080
        tax_1ad = row[5]
        tax_2ad = row[6]
        tax_22 = row[7]
        print county_id, wage_1ad, tax_22

        countyliving = CountyLiving(county_id=county_id,
                                    wage_1ad=wage_1ad,
                                    wage_2ad=wage_2ad,
                                    wage_22=wage_22,
                                    tax_1ad=tax_1ad,
                                    tax_2ad=tax_2ad,
                                    tax_22=tax_22)

        print county_id, "-", wage_1ad, "-", tax_1ad

    # We need to add to the session or it won't ever be stored
        db.session.add(countyliving)

    # # Once we're done, we should commit our work
    db.session.commit()


def load_statesliving():
    """Load cost of living by State from  into database."""

    print "Cost of Living by States"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    # Query to calculate AVG of values form maritalcounty
    StateLiving.query.delete()
    query = """ select counties.state_id as state_id,
                avg(countiesliving.wage_1ad) as wage_1ad,
                avg(countiesliving.wage_2ad) as wage_2ad,
                avg(countiesliving.wage_22) as wage_22,
                avg(countiesliving.tax_1ad) as tax_2ad,
                avg(countiesliving.tax_2ad) as tax_2ad,
                avg(countiesliving.tax_22) as tax_22
                from counties join countiesliving
                on (counties.county_id = countiesliving.county_id)
                group by counties.state_id
                order by counties.state_id
            """
    result = db.session.execute(query)

    for row in result:
        state_id = row['state_id']
        wage_1ad = row['wage_22']
        wage_2ad = row['wage_22']
        wage_22 = row['wage_22']
        tax_1ad = row['wage_22']
        tax_2ad = row['wage_22']
        tax_22 = row['wage_22']

        stateliving = StateLiving(state_id=state_id,
                                  wage_1ad=wage_1ad,
                                  wage_2ad=wage_2ad,
                                  wage_22=wage_22,
                                  tax_1ad=tax_1ad,
                                  tax_2ad=tax_2ad,
                                  tax_22=tax_22)

        print state_id, "-", wage_1ad, tax_1ad

#     # We need to add to the session or it won't ever be stored
        db.session.add(stateliving)

    # # Once we're done, we should commit our work
    db.session.commit()


def load_statesindexliving():
    """Load index of living by State from  into database."""

    print "Index of Living by States"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    # Query to calculate AVG of values form maritalcounty
    for line in open('data/indexliving.txt'):
        name, rank, index, junk = line.strip().split("|")
        name = name.rstrip()
        rank = int(rank.strip())
        index = float(index.strip())
        state = State.query.filter(State.name.like(name)).first()
        state_id = state.state_id
        stateliving = StateLiving.query.filter_by(state_id=state_id).first()
        if stateliving is not None:
            stateliving.rank = rank
            stateliving.index = index

    # # Once we're done, we should commit our work
    db.session.commit()


def load_maritalstates():
    """Load marital status from  into database."""

    print "Marital Status by States"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    # Query to calculate AVG of values form maritalcounty
    StateMarital.query.delete()
    query = """ select counties.state_id as state_id,
            avg(countiesmarital.total_male) as total_male,
            avg(countiesmarital.total_female) as total_female,
            avg(countiesmarital.male_single_1524) as male_single_1524,
            avg(countiesmarital.male_single_2539) as male_single_2539,
            avg(countiesmarital.male_single_4059) as male_single_4059,
            avg(countiesmarital.male_single_60) as male_single_60,
            avg(countiesmarital.male_married_1524) as male_married_1524,
            avg(countiesmarital.male_married_2539) as male_married_2539,
            avg(countiesmarital.male_married_4059) as male_married_4059,
            avg(countiesmarital.male_married_60) as male_married_60,
            avg(countiesmarital.male_widowed_1524) as male_widowed_1524,
            avg(countiesmarital.male_widowed_2539) as male_widowed_2539,
            avg(countiesmarital.male_widowed_4059) as male_widowed_4059,
            avg(countiesmarital.male_widowed_60) as male_widowed_60,
            avg(countiesmarital.male_divorced_1524) as male_divorced_1524,
            avg(countiesmarital.male_divorced_2539) as male_divorced_2539,
            avg(countiesmarital.male_divorced_4059) as male_divorced_4059,
            avg(countiesmarital.male_divorced_60) as male_divorced_60,
            avg(countiesmarital.female_single_1524) as female_single_1524,
            avg(countiesmarital.female_single_2539) as female_single_2539,
            avg(countiesmarital.female_single_4059) as female_single_4059,
            avg(countiesmarital.female_single_60) as female_single_60,
            avg(countiesmarital.female_married_1524) as female_married_1524,
            avg(countiesmarital.female_married_2539) as female_married_2539,
            avg(countiesmarital.female_married_4059) as female_married_4059,
            avg(countiesmarital.female_married_60) as female_married_60,
            avg(countiesmarital.female_widowed_1524) as female_widowed_1524,
            avg(countiesmarital.female_widowed_2539) as female_widowed_2539,
            avg(countiesmarital.female_widowed_4059) as female_widowed_4059,
            avg(countiesmarital.female_widowed_60) as female_widowed_60,
            avg(countiesmarital.female_divorced_1524) as female_divorced_1524,
            avg(countiesmarital.female_divorced_2539) as female_divorced_2539,
            avg(countiesmarital.female_divorced_4059) as female_divorced_4059,
            avg(countiesmarital.female_divorced_60) as female_divorced_60
            from counties
            join countiesmarital on
            (countiesmarital.county_id=counties.county_id)
            group by counties.state_id
            order by counties.state_id
            """
    result = db.session.execute(query)

    for row in result:
        state_id = row['state_id']
        total_male = row['total_male']
        total_female = row['total_female']
        male_single_1524 = row['male_single_1524']
        male_single_2539 = row['male_single_2539']
        male_single_4059 = row['male_single_4059']
        male_single_60 = row['male_single_60']
        male_married_1524 = row['male_married_1524']
        male_married_2539 = row['male_married_2539']
        male_married_4059 = row['male_married_4059']
        male_married_60 = row['male_married_60']
        male_widowed_1524 = row['male_widowed_1524']
        male_widowed_2539 = row['male_widowed_2539']
        male_widowed_4059 = row['male_widowed_4059']
        male_widowed_60 = row['male_widowed_60']
        male_divorced_1524 = row['male_divorced_1524']
        male_divorced_2539 = row['male_divorced_2539']
        male_divorced_4059 = row['male_divorced_4059']
        male_divorced_60 = row['male_divorced_60']

        female_single_1524 = row['female_single_1524']
        female_single_2539 = row['female_single_2539']
        female_single_4059 = row['female_single_4059']
        female_single_60 = row['female_single_60']
        female_married_1524 = row['female_married_1524']
        female_married_2539 = row['female_married_2539']
        female_married_4059 = row['female_married_4059']
        female_married_60 = row['female_married_60']
        female_widowed_1524 = row['female_widowed_1524']
        female_widowed_2539 = row['female_widowed_2539']
        female_widowed_4059 = row['female_widowed_4059']
        female_widowed_60 = row['female_widowed_60']
        female_divorced_1524 = row['female_divorced_1524']
        female_divorced_2539 = row['female_divorced_2539']
        female_divorced_4059 = row['female_divorced_4059']
        female_divorced_60 = row['female_divorced_60']

        state_marital = StateMarital(state_id=state_id,
                                     total_male=total_male,
                                     total_female=total_female,
                                     male_single_1524=male_single_1524,
                                     male_single_2539=male_single_2539,
                                     male_single_4059=male_single_4059,
                                     male_single_60=male_single_60,
                                     male_married_1524=male_married_1524,
                                     male_married_2539=male_married_2539,
                                     male_married_4059=male_married_4059,
                                     male_married_60=male_married_60,
                                     male_widowed_1524=male_widowed_1524,
                                     male_widowed_2539=male_widowed_2539,
                                     male_widowed_4059=male_widowed_4059,
                                     male_widowed_60=male_widowed_60,
                                     male_divorced_1524=male_divorced_1524,
                                     male_divorced_2539=male_divorced_2539,
                                     male_divorced_4059=male_divorced_4059,
                                     male_divorced_60=male_divorced_60,
                                     female_single_1524=female_single_1524,
                                     female_single_2539=female_single_2539,
                                     female_single_4059=female_single_4059,
                                     female_single_60=female_single_60,
                                     female_married_1524=female_married_1524,
                                     female_married_2539=female_married_2539,
                                     female_married_4059=female_married_4059,
                                     female_married_60=female_married_60,
                                     female_widowed_1524=female_widowed_1524,
                                     female_widowed_2539=female_widowed_2539,
                                     female_widowed_4059=female_widowed_4059,
                                     female_widowed_60=female_widowed_60,
                                     female_divorced_1524=female_divorced_1524,
                                     female_divorced_2539=female_divorced_2539,
                                     female_divorced_4059=female_divorced_4059,
                                     female_divorced_60=female_divorced_60)

        print state_id, "-", total_male, total_female
        print state_marital

#     # We need to add to the session or it won't ever be stored
        db.session.add(state_marital)

    # # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # # Import different types of data
    load_states()
    load_counties()
    # # Only by state
    load_professions()
    # # # It must load first maritalcounties, because maritalstates calculates
    # # # the info based on it.
    load_maritalcounties()
    load_maritalstates()
    # # Delete CountyLiving
    CountyLiving.query.delete()
    load_countiesliving('data/1-1000indexes.csv')
    load_countiesliving('data/1001-2000.csv')
    load_countiesliving('data/2000-3000indexes.csv')
    # # # It must load first countiesliving, because statesliving calculates
    # # # the info based on it.
    load_statesliving()
    load_crimestate()
    load_statesindexliving()
