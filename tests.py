#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport


EVERYSPORT_APIKEY = {APIKEY}

ALLSVENSKAN_2013 = 57973

class Everysport(unittest.TestCase):

	def setUp(self):
		self.api = everysport.Api(EVERYSPORT_APIKEY)

	def test_league_events(self):		
		events = self.api.events().leagues(ALLSVENSKAN_2013).all()
		self.assertTrue(len(list(events)) >= 0)

	def test_today_events(self):
		games = list(self.api.events().today().all())
		self.assertTrue(len(games) >= 0)


	def test_upcoming_events(self):
		games = list(self.api.events().upcoming().all())
		self.assertTrue(len(games) >= 0)
	


if __name__ == '__main__':
	unittest.main()


