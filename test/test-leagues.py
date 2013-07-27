#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
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
    unittest.main()