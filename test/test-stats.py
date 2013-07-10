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


class TestStats(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)      

    def test_stats(self):        
        allsvenskan = everysport.EventStats(self.api, everysport.ALLSVENSKAN)
        self.assertTrue(allsvenskan)

  
    def test_trend(self):
        allsvenskan = everysport.EventStats(self.api, everysport.ALLSVENSKAN)
        trend = allsvenskan.trend()
        self.assertTrue(trend)


    def test_trend_nhl(self):
        nhl = everysport.EventStats(self.api, everysport.NHL)
        trend = nhl.trend()
        self.assertTrue(trend)


    def test_get_pos_change(self):
        allsvenskan = everysport.EventStats(self.api, everysport.ALLSVENSKAN)
        pos1 = allsvenskan.get_team_position_by_round(2, everysport.TEAM_HBG)
        pos2 = allsvenskan.get_team_position_by_round(3, everysport.TEAM_HBG)
        change = allsvenskan.get_position_change(3, everysport.TEAM_HBG)
        self.assertEqual(change, pos1-pos2)

    def test_get_pos_by_round(self):
        allsvenskan = everysport.EventStats(self.api, everysport.ALLSVENSKAN)
        pos = allsvenskan.get_team_position_by_round(2, everysport.TEAM_HBG)
        self.assertEqual(pos, 3)

    def test_get_pos_by_round_nhl(self):
        nhl = everysport.EventStats(self.api, everysport.NHL)
        pos = nhl.get_team_position_by_round(33, everysport.TEAM_CHI)
        self.assertEqual(pos, 1)

    def test_teams(self):
        allsvenskan_skane = everysport.EventStats(self.api, everysport.ALLSVENSKAN, everysport.TEAM_HBG, everysport.TEAM_MFF)
        trend = allsvenskan_skane.trend()
        self.assertTrue(trend)




if __name__ == '__main__': 
    logging.basicConfig(filename='test-stats.log',
                            level=logging.DEBUG, 
                            filemode="w")
    unittest.main()