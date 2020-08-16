#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport
import os


class TestApi(unittest.TestCase):

    def setUp(self):        
        self.apikey = os.environ['EVERYSPORT_APIKEY'] 

    def test_api(self):
        es = everysport.Everysport(self.apikey)
        self.assertTrue(es)


if __name__ == '__main__': 
    unittest.main()