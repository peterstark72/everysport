#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import everysport
import logging
import os

'''Getting the Everysport APIKEY from the system environment. 

You need to set this with: 

    export EVERYSPORT_APIKEY={YOUR KEY}
'''
APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestStandings(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)


    def test_standings(self):
        for standings in self.api.standings(everysport.ALLSVENSKAN).fetchall():
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)   


    def test_standings2(self):

        standings = self.api.standings(everysport.ALLSVENSKAN).fetchall()
        self.assertTrue(len(standings.group().labels) >= 0)
        self.assertTrue(len(standings.group().standings) >= 0)    



    def test_standings_swiss(self):
        for standings in self.api.standings(everysport.SWISS_LEAGUE).fetchall():
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)  


    def test_get_teamposition(self):
        standings = self.api.standings(everysport.ALLSVENSKAN).round(15).fetchall()
        pos = standings.get_teamposition(everysport.HBG.id)
        self.assertEqual(pos, 3)


    def test_get_teamposition2(self):
        standings = self.api.standings(everysport.ALLSVENSKAN).round(15).fetchall()
        pos = standings.get_teamposition(666666) #Invalid
        self.assertTrue(pos == None)

    

if __name__ == '__main__': 
    logging.basicConfig(filename='standings.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()