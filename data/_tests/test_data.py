import unittest
import os
import requests
from requests.auth import HTTPBasicAuth
import glob 

class DataTest(unittest.TestCase):
    def setUp(self):
        """
        Setup variables for testing the correct abilities get loaded into the Caldera app via this
            plugin.
        
        """
        

    def test_ability_count(self):
        """
        Function that tests the amount of ablities is displayed correctly in the Caldera app.

        Will parse abilities/*/*.yml files and compare to app count via console outputs.
        
        """
        try:
            url = 'http//:localhost:8888/api/v2/abilities'
            api_data = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'))

        except requests.exceptions.HTTPError as error:
            print(error)

        arsenal_abilities = [ability["plugin"] == 'arsenal' for ability in api_data.json()]

        plugin_abilities = glob.glob('plugins/abilties/*/*.yml')

        self.assertEqual(len(arsenal_abilities), len(plugin_abilities),
                            msg=f"{plugin_abilities} abilities should  be found, but "
                                f"only {arsenal_abilities} abilities are being collected by CALDERA."   
                        )
                