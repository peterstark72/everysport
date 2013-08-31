#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import logging




import everysport



class TestEvents(unittest.TestCase):

    def setUp(self):        
        self.es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'] )


    def test_single_event(self):
        ev = self.es.get_event(2129667)
        self.assertEqual(ev['id'], 2129667)

    
    def test_events_allsvenskan(self):
        events = self.es.get_events_for_league(everysport.ALLSVENSKAN).fetch()
        self.assertTrue(len(events) == 240) #games in Allsvenskan  

    def test_events_nhl(self):
        events = self.es.get_events_for_league(everysport.NHL).fetch()
        self.assertTrue(len(events) == 720) #games in NHL 


    def test_sport(self):
        football  = self.es.events.football().today().fetch()
        self.assertTrue(football)



    

if __name__ == '__main__': 
    logging.basicConfig(filename=__file__+'.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()