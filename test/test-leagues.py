#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging
import os


import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestLeagues(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)


    def test_allsvenskan(self):
        allsvenskan = self.api.league(everysport.ALLSVENSKAN)
        self.assertTrue(allsvenskan)   



    

if __name__ == '__main__': 
    logging.basicConfig(filename='test-leagues.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()