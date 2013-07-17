#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport
import logging
import os

from everysport.encoders import json_dumps


#Getting the Everysport APIKEY from the system environment. 
APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestEncoders(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)  


    def test_json(self):
        results = self.api.get_results(everysport.ALLSVENSKAN)
        js = json_dumps(results)
        logging.debug(js)
        self.assertTrue(len(js) > 0)




if __name__ == '__main__': 
    logging.basicConfig(filename='encoders.log',
                            level=logging.DEBUG, 
                            filemode="w")
    unittest.main()
