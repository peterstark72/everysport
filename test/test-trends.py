#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

import logging
import everysport
import everysport.trends


class TestTrends(unittest.TestCase):

    def setUp(self):        
        self.es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'] )
        

    def test_allsvenskan(self):
        allsvenskan = self.es.getleague_by_name("Allsvenskan", "Football")
        trend = everysport.trends.positiontrend(self.es, allsvenskan)
        logging.debug(trend)
        self.assertTrue(trend)

        

if __name__ == '__main__': 
    logging.basicConfig(filename= __file__ + '.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()