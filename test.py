#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import everysport


'''
Getting the Everysport APIKEY from the system environment. You need to set this with 

    export EVERYSPORT_APIKEY={YOUR KEY}

'''
import os
APIKEY = os.environ['EVERYSPORT_APIKEY']


SWISS_LEAGUE = 58882
ALLSVENSKAN = 57973
SUPERETTAN = 57974
SHL = 60243
LEKSAND = 3930
NHL = 58878


class TestEndpints(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)


    def test_unauthorized(self):
        foo = everysport.Api("foo")
        with self.assertRaises(everysport.EverysportException):
            foo.events().load(2129667)



    # Events

    def test_single_event(self):
        ev = self.api.events().load(2129667)
        self.assertEqual(ev.id, 2129667)

    def test_events_allsvenskan(self):
        counter = 0
        for ev in self.api.events().leagues(ALLSVENSKAN):
            counter += 1
        self.assertTrue(counter == 240) #games in Allsvenskan  

    def test_events_allsvenskan_superettan(self):
        counter = 0
        for ev in self.api.events().leagues(ALLSVENSKAN, SUPERETTAN):
            counter += 1
        self.assertTrue(counter == 480) #games in Allsvenskan  + Superettan


    
    def test_scores(self):
        for ev in self.api.events().finished().leagues(ALLSVENSKAN):    
            self.assertTrue(int(ev.home_team_score) >= 0)    
            self.assertTrue(int(ev.visiting_team_score) >= 0)

    def test_teams(self):
        for ev in self.api.events().leagues(ALLSVENSKAN):    
            self.assertTrue(len(ev.home_team.name) > 0 )    
            self.assertTrue(len(ev.visiting_team.name) > 0 )


    def test_round(self):
        for ev in self.api.events().round(3).leagues(ALLSVENSKAN):    
            self.assertEqual(ev.round, 3)  

    def test_rounds(self):
        for ev in self.api.events().round(3,4,5,6).leagues(ALLSVENSKAN):    
            self.assertTrue(ev.round >=3 or ev.round <= 6)  


    def test_team(self):
        for ev in self.api.events().teams(LEKSAND).leagues(SHL):
            self.assertTrue(LEKSAND in (ev.home_team.id, ev.visiting_team.id))  

    def test_finished(self):
        for ev in self.api.events().finished().leagues(ALLSVENSKAN):
            self.assertEqual(ev.status, "FINISHED")    

    def test_upcoming(self):
        for ev in self.api.events().upcoming().leagues(ALLSVENSKAN):
            self.assertEqual(ev.status, "UPCOMING")    


    # Standings            

    def test_standings(self):
        for standings in self.api.standings().league(ALLSVENSKAN).load():
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)    

    def test_standings_swiss(self):
        for standings in self.api.standings().league(SWISS_LEAGUE).load():
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)  

    
    # Sports            

    def test_sports(self):        
        self.assertTrue(everysport.FOOTBALL == 10)




if __name__ == '__main__':  
    unittest.main()