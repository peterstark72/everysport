#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os


import everysport

class TestStandings(unittest.TestCase):

    def setUp(self):        
        self.es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'])
        

    def test_allsvenskan(self):
        allsvenskan = self.es.get_standings(everysport.ALLSVENSKAN)
        self.assertTrue(allsvenskan) 


    def test_teams(self):
        allsvenskan = self.es.get_standings(everysport.ALLSVENSKAN)
        self.assertTrue(allsvenskan.teams) 


    def test_round(self):
        allsvenskan = self.es.get_standings(
                            everysport.ALLSVENSKAN, 
                            r=1)
        self.assertTrue(allsvenskan) 


    def test_type(self):
        allsvenskan = self.es.get_standings(
                            everysport.ALLSVENSKAN, 
                            r=1, 
                            t="home")
        self.assertTrue(allsvenskan) 



if __name__ == '__main__': 
    unittest.main()