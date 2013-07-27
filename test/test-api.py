#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport
import os


class TestApi(unittest.TestCase):

    def setUp(self):        
        self.apikey = os.environ['EVERYSPORT_APIKEY'] 


    def test_api(self):
        api = everysport.Api(self.apikey)
        self.assertTrue(api)

    def test_api2(self):
        api = everysport.Api("foo")
        with self.assertRaises(everysport.EverysportException):
            api.league(everysport.ALLSVENSKAN)



if __name__ == '__main__': 
    unittest.main()