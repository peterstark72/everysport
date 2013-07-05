#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport

import os
APIKEY = os.environ['EVERYSPORT_APIKEY']


class TestEndpints(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(APIKEY)

    def test_single_event(self):
        ev = self.api.events().get(2129667)
        self.assertTrue(ev.id, 2129667)


    def test_events(self):
        ev = list(self.api.events().get_all(57973))     
        self.assertTrue(len(ev) > 0)    


    def test_finished(self):
        for ev in self.api.events().finished().get_all(57973):
            self.assertTrue(ev.status, "FINISHED")    

    def test_upcoming(self):
        for ev in self.api.events().upcoming().get_all(57973):
            self.assertTrue(ev.status, "UPCOMING")    


    def test_standings(self):
        ev = self.api.standings().get(57973)
        self.assertTrue(len(ev) > 0)    


if __name__ == '__main__':  
    unittest.main()