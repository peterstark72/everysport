#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging
import os


import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestStandings(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)


    def test_allsvenskan(self):
        allsvenskan = self.api.standings(everysport.ALLSVENSKAN)
        self.assertTrue(list(allsvenskan))   


    def test_swiss(self):
        swiss = self.api.standings(everysport.SWISS_LEAGUE)
        self.assertTrue(list(swiss))


    def test_get_teamposition(self):
        allsvenskan = self.api.standings(everysport.ALLSVENSKAN).round(16).list()
        pos, _ = allsvenskan.get_teamposition_and_stats(everysport.MFF)
        self.assertEqual(pos, 1)


    

if __name__ == '__main__': 
    logging.basicConfig(filename='leagues.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()