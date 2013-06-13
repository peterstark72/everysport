#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport


EVERYSPORT_APIKEY = "{API_KEY}"


class Everysport(unittest.TestCase):

	def setUp(self):
		self.api = everysport.Api(EVERYSPORT_APIKEY)

	def test_league_events(self):		
		events = self.api.events().leagues(everysport.ALLSVENSKAN_2013).load()
		self.assertTrue(len(list(events)) >= 0)

	def test_today(self):
		games = list(self.api.events().today().load())
		self.assertTrue(len(games) >= 0)

	def test_sports(self):
		sports = self.api.sports().load()
		self.assertTrue (len(list(sports)) >= 0)

	@unittest.skip('too much data')	
	def test_leagues(self):
		leagues = self.api.leagues().load()
		self.assertTrue(len(list(leagues)) >= 0)


if __name__ == '__main__':
	unittest.main()


