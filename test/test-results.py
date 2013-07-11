#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import everysport
import logging
import os



#Getting the Everysport APIKEY from the system environment. 
APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestResults(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)  


    def test_get_pos_change(self):
        
        standings = self.api.standings(everysport.ALLSVENSKAN)

        pos1 = everysport.stats.get_position_for_round(
                            standings, everysport.HBG.id, 2)
        pos2 = everysport.stats.get_position_for_round(
                            standings, everysport.HBG.id, 3)
        
        change = everysport.stats.get_position_change(
                            standings, everysport.HBG.id, 2, 3)

        self.assertEqual(change, pos1 - pos2)


    def test_results_allsvenskan(self):
        events = self.api.events().leagues(everysport.ALLSVENSKAN)
        teams = self.api.teams(everysport.ALLSVENSKAN)

        sl = everysport.stats.results(self.api, events, *teams)

        self.assertTrue(len(sl) > 0)


    def test_results_mff(self):
        events = self.api.events().leagues(everysport.ALLSVENSKAN)

        sl = everysport.stats.results(self.api, events, everysport.MFF)

        self.assertTrue(len(sl) > 0)



if __name__ == '__main__': 
    logging.basicConfig(filename='results.log',
                            level=logging.DEBUG, 
                            filemode="w")
    unittest.main()
