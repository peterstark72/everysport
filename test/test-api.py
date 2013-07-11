#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import everysport
import datetime
import logging
import os

'''Getting the Everysport APIKEY from the system environment. 

You need to set this with: 

    export EVERYSPORT_APIKEY={YOUR KEY}
'''
APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestApi(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)


    # Access control

    def test_unauthorized(self):
        foo = everysport.Api("foo")
        with self.assertRaises(everysport.EverysportException):
            foo.get_event(2129667)

    # Events

    def test_single_event(self):
        ev = self.api.get_event(2129667)
        self.assertEqual(ev.id, 2129667)

    def test_events_allsvenskan(self):
        counter = 0
        for ev in self.api.events().leagues(everysport.ALLSVENSKAN):
            counter += 1
        self.assertTrue(counter == 240) #games in Allsvenskan  


    @unittest.skip('Takes time')
    def test_events_nhl(self):
        counter = 0
        for ev in self.api.events().leagues(everysport.NHL):
            counter += 1
        self.assertTrue(counter == 720) #games in NHL  

    @unittest.skip('Takes time')
    def test_events_allsvenskan_superettan(self):
        counter = 0
        for ev in self.api.events().leagues(
                        everysport.ALLSVENSKAN, 
                        everysport.SUPERETTAN):
            counter += 1
        self.assertTrue(counter == 480) #games in Allsvenskan  + Superettan

    
    def test_scores(self):
        for ev in self.api.events().finished().leagues(
                                            everysport.ALLSVENSKAN):    
            self.assertTrue(int(ev.home_team_score) >= 0)    
            self.assertTrue(int(ev.visiting_team_score) >= 0)

    def test_teams(self):
        for ev in self.api.events().leagues(
                                            everysport.ALLSVENSKAN):    
            self.assertTrue(len(ev.home_team.name) > 0 )    
            self.assertTrue(len(ev.visiting_team.name) > 0 )


    def test_round(self):
        for ev in self.api.events().round(3).leagues(
                                            everysport.ALLSVENSKAN):    
            self.assertEqual(ev.round, 3)  

    def test_rounds(self):
        for ev in self.api.events().round(3,4,5,6).leagues(
                                            everysport.ALLSVENSKAN):    
            self.assertTrue(ev.round >=3 or ev.round <= 6)  


    def test_team(self):
        for ev in self.api.events().teams(everysport.LSD.id).leagues(everysport.SHL):
            self.assertTrue(everysport.LSD.id in (ev.home_team.id, ev.visiting_team.id))  

    

    # Events status

    def test_finished(self):
        for ev in self.api.events().finished().leagues(
                                        everysport.ALLSVENSKAN):
            self.assertEqual(ev.status, "FINISHED")    

    def test_upcoming(self):
        for ev in self.api.events().upcoming().leagues(
                                    everysport.ALLSVENSKAN):
            self.assertEqual(ev.status, "UPCOMING")    


    # Events date

    def test_fromdate(self): 
        allsvenskan = self.api.events().leagues(everysport.ALLSVENSKAN)
        today = datetime.datetime.today()

        for ev in allsvenskan.fromdate(today):
            self.assertTrue(ev.start_date >= today)
            self.assertTrue(ev.time_zone == "CEST")


    # Standings            

    def test_standings(self):
        for standings in self.api.standings(everysport.ALLSVENSKAN):
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)    

    def test_standings_swiss(self):
        for standings in self.api.standings(everysport.SWISS_LEAGUE):
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)  

    
    def test_teamslist(self):
        teams = self.api.teams(everysport.ALLSVENSKAN)
        self.assertTrue(len(teams) > 0)






if __name__ == '__main__': 
    logging.basicConfig(filename='api.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()