#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport
import logging
import os

'''Getting the Everysport APIKEY from the system environment. 

You need to set this with: 

    export EVERYSPORT_APIKEY={YOUR KEY}
'''
APIKEY = os.environ['EVERYSPORT_APIKEY'] 


class TestApi(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)

    
    def test_teamslist(self):
        teams = self.api.get_teams(everysport.ALLSVENSKAN)
        self.assertTrue(len(teams) > 0)


if __name__ == '__main__': 
    logging.basicConfig(filename='teams.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()