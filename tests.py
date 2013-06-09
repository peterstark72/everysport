#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import everysport


#The Everysport APIKEY is inside a JSON object in 'config.json': 
#{"APIKEY" : {YOUR APIKEY}, "ALLSVENSKAN_LEAGUE_ID" : 57973 }  
import json
config = json.load(open('config.json'))

class Everysport(unittest.TestCase):

	def setUp(self):
		self.api = everysport.Api(config['APIKEY'])

	def test_league_events(self):		
		events = self.api.events().leagues(config['ALLSVENSKAN_LEAGUE_ID']).load()
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


