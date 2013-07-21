#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport
import logging
import os

APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestApi(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)


    def test_api(self):
        self.assertTrue(self.api)

    def test_unauthorized(self):
        foo = everysport.Api("foo")
        with self.assertRaises(everysport.EverysportException):
            foo.event(2129667).get()



if __name__ == '__main__': 
    unittest.main()