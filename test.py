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
SHL = 60243
LEKSAND = 3930


class TestEndpints(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)

    def test_single_event(self):
        ev = self.api.events().get(2129667)
        self.assertEqual(ev.id, 2129667)

    def test_events_allsvenskan(self):
        ev = list(self.api.events().get_all(ALLSVENSKAN))     
        self.assertTrue(len(ev) > 0)  

    
    def test_scores(self):
        for ev in self.api.events().finished().get_all(ALLSVENSKAN):    
            self.assertTrue(int(ev.home_team_score) >= 0)    
            self.assertTrue(int(ev.visiting_team_score) >= 0)

    def test_teams(self):
        for ev in self.api.events().get_all(ALLSVENSKAN):    
            self.assertTrue(len(ev.home_team.name) > 0 )    
            self.assertTrue(len(ev.visiting_team.name) > 0 )


    def test_round(self):
        for ev in self.api.events().round(3).get_all(ALLSVENSKAN):    
            self.assertEqual(ev.round, 3)  

    def test_rounds(self):
        for ev in self.api.events().round(3,4,5,6).get_all(ALLSVENSKAN):    
            self.assertTrue(ev.round >=3 or ev.round <= 6)  


    def test_team(self):
        for ev in self.api.events().teams(LEKSAND).get_all(SHL):
            self.assertTrue(LEKSAND in (ev.home_team.id, ev.visiting_team.id))  

    def test_finished(self):
        for ev in self.api.events().finished().get_all(ALLSVENSKAN):
            self.assertEqual(ev.status, "FINISHED")    

    def test_upcoming(self):
        for ev in self.api.events().upcoming().get_all(ALLSVENSKAN):
            self.assertEqual(ev.status, "UPCOMING")    


    def test_standings(self):
        ev = self.api.standings().get(ALLSVENSKAN)
        self.assertTrue(len(ev) > 0)    

    def test_standings_swiss(self):
        ev = list(self.api.standings().get(SWISS_LEAGUE))     
        self.assertTrue(len(ev) > 0)  



if __name__ == '__main__':  
    unittest.main()