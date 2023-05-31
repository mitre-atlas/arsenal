import unittest
import requests
import glob 

class DataTest(unittest.TestCase):
    def setUp(self):
        """
        Setup variables for testing the correct abilities get loaded into the Caldera app via this
            plugin.
        
        """
        try:
            with requests.Session() as session:
                self.post = session.post('http://0.0.0.0:8888/enter', data=dict(username='admin', password='admin'))
                self.api_abilities = session.get(self.post.url+'api/v2/abilities')
                self.api_adversaries = session.get(self.post.url+'api/v2/adversaries')
            
        except requests.exceptions.HTTPError as error:
            print(error)
        

    def test_ability_count(self):
        """
        Function that tests the amount of ablities is displayed correctly in the Caldera app.

        Will parse abilities/*/*.yml files and compare to app count via console outputs.

        TODO: include tests for matching the yaml files so we know which abilities need fixing
        
        """
        
        all_abilities = self.api_abilities.json()
        arsenal_abilities = [all_abilities[x]['ability_id'] for x in range(len(all_abilities)) if all_abilities[x]['plugin'] == 'arsenal']

        plugin_abilities = glob.glob('/usr/src/app/plugins/arsenal/data/abilities/*/*.yml')

        self.assertEqual(len(arsenal_abilities), len(plugin_abilities),
                            msg=f"{plugin_abilities} abilities should  be found, but "
                                f"only {arsenal_abilities} abilities are being collected by CALDERA."   
                        )

    def test_adversary_count(self):
        """
        Function that tests the amount of adversaries is displayed correctly in the Caldera app.

        Will parse adversaries/*/*.yml files and compare to app count via console outputs.

        TODO: include tests for matching the yaml files so we know which abilities need fixing
        
        """
        
        all_adversaries = self.api_adversaries.json()
        arsenal_adversaries = [all_adversaries[x]['ability_id'] for x in range(len(all_adversaries)) if all_adversaries[x]['plugin'] == 'arsenal']

        plugin_adversaries = glob.glob('/usr/src/app/plugins/arsenal/data/adversaries/*/*.yml')

        self.assertEqual(len(arsenal_adversaries), len(plugin_adversaries),
                            msg=f"{plugin_adversaries} abilities should  be found, but "
                                f"only {arsenal_adversaries} abilities are being collected by CALDERA."   
                        )     