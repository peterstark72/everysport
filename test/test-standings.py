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
        for standings in self.api.standings(everysport.ALLSVENSKAN).getall():
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)   


    def test_standings2(self):

        standings = self.api.standings(everysport.ALLSVENSKAN).getall()
        self.assertTrue(len(standings[0].labels) >= 0)
        self.assertTrue(len(standings[0].standings) >= 0)    



    def test_standings_swiss(self):
        for standings in self.api.standings(everysport.SWISS_LEAGUE).getall():
            self.assertTrue(len(standings.labels) >= 0)    
            self.assertTrue(len(standings) > 0)  

    

if __name__ == '__main__': 
    logging.basicConfig(filename='standings.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()