#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import logging
import datetime


import everysport



class TestEvents(unittest.TestCase):

    def setUp(self):        
        self.es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'] )


    def test_single_event(self):
        ev = self.es.getevent(2129667)
        self.assertEqual(ev.id, 2129667)

    
    def test_events_allsvenskan(self):
        events = self.es.events.leagues(everysport.ALLSVENSKAN).fetch()
        self.assertTrue(len(events) == 240) #games in Allsvenskan  

    @unittest.skip("Takes for ever")        
    def test_events_nhl(self):
        events = self.es.events.leagues(everysport.NHL).fetch()
        self.assertTrue(len(events) == 720) #games in NHL 


    def test_sport(self):
        football  = self.es.events.football()
        self.assertTrue(football)



    def test_today(self):
        events_today = self.es.events.today().fetch()
        for event in events_today:
            self.assertEqual(event.start_date.day, datetime.datetime.today().day)

    

if __name__ == '__main__': 
    logging.basicConfig(filename=__file__+'.log', 
                        level=logging.DEBUG, 
                        filemode="w") 
    unittest.main()