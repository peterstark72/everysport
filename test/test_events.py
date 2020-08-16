import unittest
import os
import logging
import everysport


class TestEvents(unittest.TestCase):

    def setUp(self):        
        self.es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'])

    def test_events(self):
        events = self.es.get_events_for_league(everysport.ALLSVENSKAN).fetch()
        self.assertTrue(len(events) > 0)

    def test_sport(self):
        football = self.es.events.football().today().fetch()
        self.assertTrue(football)

if __name__ == '__main__': 
    unittest.main()