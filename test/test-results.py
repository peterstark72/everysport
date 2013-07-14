#!/usr/bin/env python
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


    def test_results_allsvenskan(self):
        results = self.api.get_results(everysport.ALLSVENSKAN)
        self.assertTrue(len(list(results)) > 0)

    @unittest.skip("Takes time")        
    def test_results_nhl(self):
        results = self.api.get_results(everysport.NHL)
        self.assertTrue(len(list(results)) > 0)



if __name__ == '__main__': 
    logging.basicConfig(filename='results.log',
                            level=logging.DEBUG, 
                            filemode="w")
    unittest.main()
