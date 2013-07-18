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

        results_as_list = list(results)        

        number_of_teams = len(results_as_list)

        logging.debug(results_as_list)

        self.assertTrue(number_of_teams > 0)


        

    


if __name__ == '__main__': 
    logging.basicConfig(filename='results.log',
                            level=logging.DEBUG, 
                            filemode="w")
    unittest.main()
