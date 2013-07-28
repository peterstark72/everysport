#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport
import os

from everysport.league import ALLSVENSKAN


class TestApi(unittest.TestCase):

    def setUp(self):        
        self.apikey = os.environ['EVERYSPORT_APIKEY'] 


    def test_api(self):
        es = everysport.Everysport(self.apikey)
        self.assertTrue(es)

    def test_api2(self):
        es = everysport.Everysport("foo")
        with self.assertRaises(everysport.EverysportException):
            es.getleague(ALLSVENSKAN)



if __name__ == '__main__': 
    unittest.main()