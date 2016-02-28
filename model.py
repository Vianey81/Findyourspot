"""Models and database functions for Find your spot project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class State(db.Model):
    """States of Find your spot Website."""

    __tablename__ = "states"

    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    short_name = db.Column(db.String(4), nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    percapita_income = db.Column(db.Float, nullable=True, default=0)
    median_household_income = db.Column(db.Float, nullable=True, default=0)
    population = db.Column(db.Float, nullable=True, default=0)
    number_households = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<State state_id=%s name=%s>" % (self.state_id, self.name)


class County(db.Model):
    """Counties of Find your spot website."""

    __tablename__ = "counties"

    county_id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey("states.state_id"))
    name = db.Column(db.String(100), nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    percapita_income = db.Column(db.Float, nullable=True, default=0)
    median_household_income = db.Column(db.Float, nullable=True, default=0)
    population = db.Column(db.Float, nullable=True, default=0)
    number_households = db.Column(db.Integer, nullable=True, default=0)

    #Define the relationship to the State
    state = db.relationship("State",
                            backref=db.backref("counties", order_by=county_id))


# class StatePopulation(db.Model):
#     """Population data of Find your spot website."""

#     __tablename__ = "statespopulation"

#     spop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
#     med_female_age = db.Column(db.Integer, nullable=True)
#     med_male_age = db.Column(db.Integer, nullable=True)
#     population = db.Column(db.Integer, nullable=True)
#     pop_white = db.Column(db.Integer, nullable=True)
#     pop_black = db.Column(db.Integer, nullable=True)
#     pop_hispanic = db.Column(db.Integer, nullable=True)
#     pop_other = db.Column(db.Integer, nullable=True)
#     pop_hawaiian = db.Column(db.Integer, nullable=True)
#     med_home_value = db.Column(db.Integer, nullable=True)
#     med_gross_rent = db.Column(db.Integer, nullable=True)
#     med_commute = db.Column(db.Integer, nullable=True)
#     med_income = db.Column(db.Integer, nullable=True)
#     poverty_rate = db.Column(db.Integer, nullable=True)

#     #Define relationship to the State
#     state = db.relationship("State",
#                             backref=db.backref("population", order_by=spop_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Population by State pop_id=%s state_id=%s>" % (
#             self.spop_id, self.state_id)


# class CountyPopulation(db.Model):
#     """Population data by County of Find your spot website."""

#     __tablename__ = "countiespopulation"

#     cpop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     county_id = db.Column(db.Integer, db.ForeignKey('counties.county_id'))
#     med_female_age = db.Column(db.Integer, nullable=True)
#     med_male_age = db.Column(db.Integer, nullable=True)
#     population = db.Column(db.Integer, nullable=True)
#     pop_white = db.Column(db.Integer, nullable=True)
#     pop_black = db.Column(db.Integer, nullable=True)
#     pop_hispanic = db.Column(db.Integer, nullable=True)
#     pop_other = db.Column(db.Integer, nullable=True)
#     pop_hawaiian = db.Column(db.Integer, nullable=True)
#     med_home_value = db.Column(db.Integer, nullable=True)
#     med_gross_rent = db.Column(db.Integer, nullable=True)
#     med_commute = db.Column(db.Integer, nullable=True)
#     med_income = db.Column(db.Integer, nullable=True)
#     poverty_rate = db.Column(db.Integer, nullable=True)

#     #Define relationship to the State
#     county = db.relationship("County",
#                              backref=db.backref("population", order_by=cpop_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Population by County pop_id=%s state_id=%s>" % (
#             self.cpop_id, self.county_id)


class StateProfession(db.Model):
    """Profession data by State of Find your spot website."""

    __tablename__ = "statesprofessions"

    sprof_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    title = db.Column(db.String(255), nullable=True)
    a_mean = db.Column(db.Float, nullable=True, default=0)
    jobs_1000 = db.Column(db.Float, nullable=True, default=0)
    level = db.Column(db.String(100), nullable=True)

    #Define relationship to the State
    state = db.relationship("State",
                            backref=db.backref("professions", order_by=sprof_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Professions by State sprof_id=%s state_id=%s>" % (
            self.sprof_id, self.state_id)


class StateLiving(db.Model):
    """Cost of living data by State of Find your spot website."""

    __tablename__ = "statesliving"

    sliv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    wage_1ad = db.Column(db.Float, nullable=True, default=0)
    wage_2ad = db.Column(db.Float, nullable=True, default=0)
    wage_22 = db.Column(db.Float, nullable=True, default=0)
    tax_1ad = db.Column(db.Float, nullable=True, default=0)
    tax_2ad = db.Column(db.Float, nullable=True, default=0)
    tax_22 = db.Column(db.Float, nullable=True, default=0)
    rank = db.Column(db.Integer, nullable=True, default=0)
    index = db.Column(db.Float, nullable=True, default=0)

    #Define relationship to the State
    state = db.relationship("State",
                            backref=db.backref("livings", order_by=sliv_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Cost of living by State sliv_id=%s state_id=%s>" % (
            self.sliv_id, self.state_id)


class CountyLiving(db.Model):
    """Cost of living data by County of Find your spot website."""

    __tablename__ = "countiesliving"

    cliv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.county_id'))
    wage_1ad = db.Column(db.Float, nullable=True, default=0)
    wage_2ad = db.Column(db.Float, nullable=True, default=0)
    wage_22 = db.Column(db.Float, nullable=True, default=0)
    tax_1ad = db.Column(db.Float, nullable=True, default=0)
    tax_2ad = db.Column(db.Float, nullable=True, default=0)
    tax_22 = db.Column(db.Float, nullable=True, default=0)
    rank = db.Column(db.Integer, nullable=True, default=0)
    index = db.Column(db.Float, nullable=True, default=0)

    #Define relationship to the County
    county = db.relationship("County",
                             backref=db.backref("livings", order_by=cliv_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Cost of living by County cliv_id=%s state_id=%s>" % (
            self.cliv_id, self.county_id)


class StateMarital(db.Model):
    """Cost of living data by State of Find your spot website."""

    __tablename__ = "statesmarital"

    smar_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    total_male = db.Column(db.Integer, nullable=True)
    total_female = db.Column(db.Integer, nullable=True)
    male_single_1524 = db.Column(db.Float, nullable=True)
    male_single_2539 = db.Column(db.Float, nullable=True)
    male_single_4059 = db.Column(db.Float, nullable=True)
    male_single_60 = db.Column(db.Float, nullable=True)
    male_married_1524 = db.Column(db.Float, nullable=True)
    male_married_2539 = db.Column(db.Float, nullable=True)
    male_married_4059 = db.Column(db.Float, nullable=True)
    male_married_60 = db.Column(db.Float, nullable=True)
    male_widowed_1524 = db.Column(db.Float, nullable=True)
    male_widowed_2539 = db.Column(db.Float, nullable=True)
    male_widowed_4059 = db.Column(db.Float, nullable=True)
    male_widowed_60 = db.Column(db.Float, nullable=True)
    male_divorced_1524 = db.Column(db.Float, nullable=True)
    male_divorced_2539 = db.Column(db.Float, nullable=True)
    male_divorced_4059 = db.Column(db.Float, nullable=True)
    male_divorced_60 = db.Column(db.Float, nullable=True)

    female_single_1524 = db.Column(db.Float, nullable=True)
    female_single_2539 = db.Column(db.Float, nullable=True)
    female_single_4059 = db.Column(db.Float, nullable=True)
    female_single_60 = db.Column(db.Float, nullable=True)
    female_married_1524 = db.Column(db.Float, nullable=True)
    female_married_2539 = db.Column(db.Float, nullable=True)
    female_married_4059 = db.Column(db.Float, nullable=True)
    female_married_60 = db.Column(db.Float, nullable=True)
    female_widowed_1524 = db.Column(db.Float, nullable=True)
    female_widowed_2539 = db.Column(db.Float, nullable=True)
    female_widowed_4059 = db.Column(db.Float, nullable=True)
    female_widowed_60 = db.Column(db.Float, nullable=True)
    female_divorced_1524 = db.Column(db.Float, nullable=True)
    female_divorced_2539 = db.Column(db.Float, nullable=True)
    female_divorced_4059 = db.Column(db.Float, nullable=True)
    female_divorced_60 = db.Column(db.Float, nullable=True)

    #Define relationship to the State
    state = db.relationship("State",
                            backref=db.backref("marital", order_by=smar_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Marital Status by State smar_id=%s state_id=%s>" % (
            self.smar_id, self.state_id)


class CountyMarital(db.Model):
    """Marital Status data by County of Find your spot website."""

    __tablename__ = "countiesmarital"

    cmar_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.county_id'))
    total_male = db.Column(db.Integer, nullable=True)
    total_female = db.Column(db.Integer, nullable=True)
    male_single_1524 = db.Column(db.Float, nullable=True)
    male_single_2539 = db.Column(db.Float, nullable=True)
    male_single_4059 = db.Column(db.Float, nullable=True)
    male_single_60 = db.Column(db.Float, nullable=True)
    male_married_1524 = db.Column(db.Float, nullable=True)
    male_married_2539 = db.Column(db.Float, nullable=True)
    male_married_4059 = db.Column(db.Float, nullable=True)
    male_married_60 = db.Column(db.Float, nullable=True)
    male_widowed_1524 = db.Column(db.Float, nullable=True)
    male_widowed_2539 = db.Column(db.Float, nullable=True)
    male_widowed_4059 = db.Column(db.Float, nullable=True)
    male_widowed_60 = db.Column(db.Float, nullable=True)
    male_divorced_1524 = db.Column(db.Float, nullable=True)
    male_divorced_2539 = db.Column(db.Float, nullable=True)
    male_divorced_4059 = db.Column(db.Float, nullable=True)
    male_divorced_60 = db.Column(db.Float, nullable=True)

    female_single_1524 = db.Column(db.Float, nullable=True)
    female_single_2539 = db.Column(db.Float, nullable=True)
    female_single_4059 = db.Column(db.Float, nullable=True)
    female_single_60 = db.Column(db.Float, nullable=True)
    female_married_1524 = db.Column(db.Float, nullable=True)
    female_married_2539 = db.Column(db.Float, nullable=True)
    female_married_4059 = db.Column(db.Float, nullable=True)
    female_married_60 = db.Column(db.Float, nullable=True)
    female_widowed_1524 = db.Column(db.Float, nullable=True)
    female_widowed_2539 = db.Column(db.Float, nullable=True)
    female_widowed_4059 = db.Column(db.Float, nullable=True)
    female_widowed_60 = db.Column(db.Float, nullable=True)
    female_divorced_1524 = db.Column(db.Float, nullable=True)
    female_divorced_2539 = db.Column(db.Float, nullable=True)
    female_divorced_4059 = db.Column(db.Float, nullable=True)
    female_divorced_60 = db.Column(db.Float, nullable=True)

    #Define relationship to the County
    county = db.relationship("County",
                             backref=db.backref("marital", order_by=cmar_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Marital Status by County cmar_id=%s county_id=%s>" % (
            self.cmar_id, self.county_id)


class StateCrime(db.Model):
    """Crime data by State of Find your spot website."""

    __tablename__ = "statescrime"

    scri_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    violent_rate = db.Column(db.Float, nullable=True, default=0)
    murder_rate = db.Column(db.Float, nullable=True, default=0)
    rape_rate = db.Column(db.Float, nullable=True, default=0)
    assault_rate = db.Column(db.Float, nullable=True, default=0)
    robery_rate = db.Column(db.Float, nullable=True, default=0)
    property_rate = db.Column(db.Float, nullable=True, default=0)
    motor_rate = db.Column(db.Float, nullable=True, default=0)
    total = db.Column(db.Float, nullable=True, default=0)

    #Define relationship to the State
    state = db.relationship("State",
                            backref=db.backref("crime", order_by=scri_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Crime by State smar_id=%s state_id=%s>" % (
            self.scri_id, self.state_id)


class CountyCrime(db.Model):
    """Crime data by County of Find your spot website."""

    __tablename__ = "countiescrime"

    ccri_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.county_id'))
    violent_rate = db.Column(db.Float, nullable=True, default=0)
    murder_rate = db.Column(db.Float, nullable=True, default=0)
    rape_rate = db.Column(db.Float, nullable=True, default=0)
    assault_rate = db.Column(db.Float, nullable=True, default=0)
    robery_rate = db.Column(db.Float, nullable=True, default=0)
    property_rate = db.Column(db.Float, nullable=True, default=0)
    motor_rate = db.Column(db.Float, nullable=True, default=0)
    total = db.Column(db.Float, nullable=True, default=0)

    #Define relationship to the County
    state = db.relationship("County",
                            backref=db.backref("crime", order_by=ccri_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Crime by County ccri_id=%s county_id=%s>" % (
            self.ccri_id, self.county_id)
##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///usastatistics'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
