"""Sample test suite for testing demo."""

import ranking
from model import connect_to_db, db
from server import app
import server
import unittest
import doctest
from flask import Flask


def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests.

    This function name, ``load_tests``, is required.
    """

    tests.addTests(doctest.DocTestSuite(ranking))

    return tests


class RankingTestCase(unittest.TestCase):
    """Examples of unit tests: discrete code testing."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Create secret key to access session
        app.secret_key = "ABC"

        # Connect to fake database
        connect_to_db(app)

        app.config['TESTING'] = True

    def assert_valid_result(self, result):
        # tests if the returned object is a List
        self.assertIsInstance(result, list, "The object is not an instance of class List")

        my_keys = [u'wage', u'median_household_income', u'name', u'number_households', u'discretionary_income', u'percapita_income', u'population']
        for item in result:
            # tests if the returned list has all the columns on it
            self.assertListEqual(item.keys(), my_keys, "All the items should have all the keys")


    def test_county_Missouri(self):
        """ Test the function get_county_by_id with the case Missouri """

        county_values = {'median_household_income': 67721, 'number_households': 36781,
                    'percapita_income': 35143, 'population': 90842}
        state_id = "29"
        tax = "1ad"

        result = ranking.counties_by_id(state_id, tax)
        self.assert_valid_result(result)

        # tests if the returned list has 115 counties
        self.assertEqual(len(result), 115, "The list must have 1115 item on it")

        for item in result:
            if (item['name'] == 'Platte'):
                # tests the values for the County of Platte
                self.assertEqual(item['median_household_income'], county_values['median_household_income'], "The median_household_income is different"+str(item['median_household_income'])+" - "+ str(county_values['median_household_income'])) 
                self.assertEqual(item['number_households'], county_values['number_households'], "The number_households is different"+str(item['number_households'])+" - "+ str(county_values['number_households'])) 
                self.assertEqual(item['percapita_income'], county_values['percapita_income'], "The percapita_income is different"+str(item['percapita_income'])+" - "+ str(county_values['percapita_income'])) 
                self.assertEqual(item['population'], county_values['population'], "The population is different"+str(item['population'])+" - "+ str(county_values['population'])) 


    def test_county_Alabama(self):
        """ Test the function get_county_by_id with the case Alabama """

        county_values = {'median_household_income': 68770, 'number_households': 74144,
                    'percapita_income': 33313, 'population': 198366}
        state_id = "1"
        tax = "1ad"

        result = ranking.counties_by_id(state_id, tax)
        self.assert_valid_result(result)

        # tests if the returned list has 67 counties
        self.assertEqual(len(result), 67, "The list must have 67 item on it")

        for item in result:
            if (item['name'] == 'Shelby'):
                # tests the values for the County of Platte
                self.assertEqual(item['median_household_income'], county_values['median_household_income'], "The median_household_income is different"+str(item['median_household_income'])+" - "+ str(county_values['median_household_income'])) 
                self.assertEqual(item['number_households'], county_values['number_households'], "The number_households is different"+str(item['number_households'])+" - "+ str(county_values['number_households'])) 
                self.assertEqual(item['percapita_income'], county_values['percapita_income'], "The percapita_income is different"+str(item['percapita_income'])+" - "+ str(county_values['percapita_income'])) 
                self.assertEqual(item['population'], county_values['population'], "The population is different"+str(item['population'])+" - "+ str(county_values['population'])) 


    def test_county_Texas(self):
        """ Test the function get_county_by_id with The case Texas """

        county_values = {'median_household_income': 58025, 'number_households': 411876,
                    'percapita_income': 33206, 'population': 1063248}
        state_id = "48"
        tax = "1ad"

        result = ranking.counties_by_id(state_id, tax)
        self.assert_valid_result(result)

        # tests if the returned list has 254 counties
        self.assertEqual(len(result), 254, "The list must have 254 item on it")
        for item in result:
            if (item['name'] == 'Travis'):
                # tests the values for the County of Platte
                self.assertEqual(item['median_household_income'], county_values['median_household_income'], "The median_household_income is different"+str(item['median_household_income'])+" - "+ str(county_values['median_household_income'])) 
                self.assertEqual(item['number_households'], county_values['number_households'], "The number_households is different"+str(item['number_households'])+" - "+ str(county_values['number_households'])) 
                self.assertEqual(item['percapita_income'], county_values['percapita_income'], "The percapita_income is different"+str(item['percapita_income'])+" - "+ str(county_values['percapita_income'])) 
                self.assertEqual(item['population'], county_values['population'], "The population is different"+str(item['population'])+" - "+ str(county_values['population'])) 


    def test_legal_single_1524(self):
        """ Test the function get_top_states with the Case : Legal Occupations, Single status, 15 - 24 years old. """

        result = ranking.get_top_states("1ad", "Legal Occupations", "single_1524", 4, 4, 4, 4, professionptn='None')
        Montana = {'crimerank': 3296.1, 'professionrank': '41398.96',
                    'marRank': 16, 'livingrank': 31}
        California = {'crimerank': 4048.1, 'professionrank': '96417.76',
                    'marRank': 168, 'livingrank': 47}

        Ohio = {'crimerank': 3885.8, 'professionrank': '65523.52',
                    'marRank': 128, 'livingrank': 16}

        # tests if the returned object is a List
        print "Testing if returns a list"
        self.assertIsInstance(result, list, "The object is not an instance of class List")

        # tests if the returned list has 50 elements
        print "Testing if the returned list contains 50 elements"
        self.assertEqual(len(result), 50, "The list must have 50 items on it")

        my_keys = [u'crimerank', u'professionrank', 'Total', u'median_household_income', u'name', u'a_mean', 'marRank', u'id', u'number_households', u'totalmarital', 'personalprofession', 'professionptn', u'livingrank', 'criRank', 'LivRank', 'profRank', u'jobs_1000', u'percapita_income', 'rate', u'population']
        for item in result:
    
            # tests if the returned list has all the columns on it
            self.assertListEqual(item.keys(), my_keys, "All the items should have all the keys") 

            for key, value in item.iteritems():
                # tests that all the values not null
                self.assertGreaterEqual(value, 0, "All values must be filled")

            if (item['name'] == 'Montana'):
                # tests the calculations for Montana
                self.assertEqual(item['crimerank'], Montana['crimerank'], "The rank is different"+str(item['crimerank'])+" - "+ str(Montana['crimerank'])) 
                self.assertEqual(item['professionrank'], Montana['professionrank'], "The Profession rank is different"+str(item['professionrank'])+" - "+ str(Montana['professionrank'])) 
                self.assertEqual(item['marRank'], Montana['marRank'], "The Marital rank is different"+str(item['marRank'])+" - "+ str(Montana['marRank'])) 
                self.assertEqual(item['livingrank'], Montana['livingrank'], "The Living rank is different"+str(item['livingrank'])+" - "+ str(Montana['livingrank'])) 

            if (item['name'] == 'California'):
                # tests the calculations for California
                self.assertEqual(item['crimerank'], California['crimerank'], "The rank is different"+str(item['crimerank'])+" - "+ str(California['crimerank'])) 
                self.assertEqual(item['professionrank'], California['professionrank'], "The Profession rank is different"+str(item['professionrank'])+" - "+ str(California['professionrank'])) 
                self.assertEqual(item['marRank'], California['marRank'], "The Marital rank is different"+str(item['marRank'])+" - "+ str(California['marRank'])) 
                self.assertEqual(item['livingrank'], California['livingrank'], "The Living rank is different"+str(item['livingrank'])+" - "+ str(California['livingrank'])) 

            if (item['name'] == 'Ohio'):
                # tests the calculations for Ohio
                self.assertEqual(item['crimerank'], Ohio['crimerank'], "The rank is different"+str(item['crimerank'])+" - "+ str(Ohio['crimerank'])) 
                self.assertEqual(item['professionrank'], Ohio['professionrank'], "The Profession rank is different"+str(item['professionrank'])+" - "+ str(Ohio['professionrank'])) 
                self.assertEqual(item['marRank'], Ohio['marRank'], "The Marital rank is different"+str(item['marRank'])+" - "+ str(Ohio['marRank'])) 
                self.assertEqual(item['livingrank'], Ohio['livingrank'], "The Living rank is different"+str(item['livingrank'])+" - "+ str(Ohio['livingrank'])) 

    def test_home(self):
        result = self.client.get('/')
        # Test if the Search Form load
        self.assertIn('<i class="fa fa-search"> </i> Select your Preferences', result.data)

        # Test if the chart contaniner is in the Form
        self.assertIn('<div id="chartsbystate" class="container" hidden=true>', result.data)

        # Test if the Table is in the Form
        self.assertIn('<table id="infotable" cellspacing="0" width="100%">', result.data)

        # Test if the About section is in the Form
        self.assertIn('<h4 class="modal-title" id="myModalLabel">', result.data)

    def test_search_states(self):
        """ Test if the route in python returns a 200 code """

        profession = "Legal Occupations"
        url = "/search_states?tax=1ad&profession="+profession+"&professionptn=None&age=1524&marital=single&opcLiving=4&opcMarital=4&opcCrime=4&opcProfession=4";

        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    def test_crime_json(self):
        """ Test if the route in python returns a 200 code """

        url = "/crime.json?id=6"
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    def test_marital_json(self):
        """ Test if the route in python returns a 200 code """

        url = "/marital.json?id=6"
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    def test_age_json(self):
        """ Test if the route in python returns a 200 code """

        url = "/age.json?id=6"
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

        
    def test_search_states(self):
        """ Test if the route in python returns a 200 code """
        
        profession = "Legal Occupations"
        url = "/chartsgral.json?chart=marliv&ntop=3&tax=1ad&profession="+profession+"&professionptn=None&age=1524&marital=single&opcLiving=4&opcMarital=4&opcCrime=4&opcProfession=4";

        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

        

# class MyAppIntegrationTestCase(unittest.TestCase):
#     """Examples of integration tests: testing Flask server."""

#     def setUp(self):
#         print "(setUp ran)"
#         self.client = server.app.test_client()
#         server.app.config['TESTING'] = True

#     def tearDown(self):
#         # We don't need to do anything here; we could just
#         # not define this method at all, but we have a stub
#         # here as an example.
#         print "(tearDown ran)"

#     def test_home(self):
#         result = self.client.get('/')
#         self.assertIn('<h1>Test</h1>', result.data)

#     def test_adder(self):
#         result = self.client.get('/add-things?x=-1&y=1')
#         self.assertEqual(result.data, "99")

#     def test_results(self):
#         result = self.client.get('/')
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('<h1>Test</h1>', result.data)


if __name__ == '__main__':
    # If called like a script, run our tests

    unittest.main()
