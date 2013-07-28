#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os


import everysport
from everysport.team import MFF


class TestStandings(unittest.TestCase):

    def setUp(self):        
        self.es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'])
        

    def test_allsvenskan(self):
        allsvenskan = self.es.getleague_by_name("Allsvenskan", "Football")
        self.assertTrue(allsvenskan) 

    def test_standings(self):
        allsvenskan = self.es.getleague_by_name("Allsvenskan", "Football").round(17).standings
        self.assertTrue(2, allsvenskan.getteamposition(MFF)) 




if __name__ == '__main__': 
    unittest.main()