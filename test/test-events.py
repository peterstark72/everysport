#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport
import os
import logging




class TestEvents(unittest.TestCase):

    def setUp(self):        
        self.api = everysport.Api(os.environ['EVERYSPORT_APIKEY'] )


    def test_single_event(self):
        ev = self.api.event(2129667)
        self.assertEqual(ev.id, 2129667)

    
    def test_events_allsvenskan(self):
        events = list(self.api.events().leagues(everysport.ALLSVENSKAN))
        self.assertTrue(len(events) == 240) #games in Allsvenskan  


    def test_events_nhl(self):
        events = list(self.api.events().leagues(everysport.NHL))
        self.assertTrue(len(events) == 720) #games in NHL  
    

if __name__ == '__main__': 
    logging.basicConfig(filename='test-events.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()