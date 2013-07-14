#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import logging

import everysport.url_builder

class TestUrls(unittest.TestCase):

    def test_event(self):
        url = everysport.url_builder.get_event_url(7126276, apikey="foo")
        logging.debug(url)
        self.assertTrue(url)


    def test_events(self):
        url = everysport.url_builder.get_events_url(57282, apikey="foo")
        logging.debug(url)
        self.assertTrue(url)


    def test_events_multipleleagues(self):
        url = everysport.url_builder.get_events_url(57282, 58883, apikey="foo")
        logging.debug(url)
        self.assertTrue(url)

    def test_events_withargs(self):
        url = everysport.url_builder.get_events_url(57282, apikey="foo", round=5)
        logging.debug(url)
        self.assertTrue(url)



    def test_standings(self):
        url = everysport.url_builder.get_standings_url(57282, apikey="foo")
        logging.debug(url)
        self.assertTrue(url)



if __name__ == '__main__': 
    logging.basicConfig(filename='url.log', level=logging.DEBUG, filemode="w")
    unittest.main()