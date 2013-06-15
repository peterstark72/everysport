#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

A simple library that wraps the Everysport API. 


'''


import datetime
import urllib
import json

from data import Event
from data import Standings


BASE_API_URL = "http://api.everysport.com/v1/{}"


class Api(object):
	def __init__(self, apikey):
		self._apikey = apikey


	def events(self, event_id=None):
		if event_id:
			endpoint = 'events/' + str(event_id)
			result_json = self.get_json(endpoint)
			if result_json:
				return Event().from_json(result_json.get('event',{}))
			else:
				return None
		else:
			return EventsQuery(self)


	def standings(self, league_id):
		return StandingsQuery(self, league_id)


	def get_json(self, endpoint, params=dict()):
		
		params['apikey'] = self._apikey
		encoded_params = urllib.urlencode(params)
		url = BASE_API_URL.format(endpoint) + '?' + encoded_params	

		try:			
			response = urllib.urlopen(url)
			result = json.load(response)
		except:
			return None
		
		return result



class StandingsQuery(object):
	def __init__(self, api, league_id):
		self.api = api
		self.query = {}
		self.league_id = league_id

	def total(self):
		self.query['type'] = 'total'
		return self

	def home(self):
		self.query['type'] = 'home'
		return self		

	def away(self):
		self.query['type'] = 'away'
		return self		

	def round(self, x):
		self.query['round'] = x
		return self	

	def load(self):
		endpoint = 'leagues/' + str(self.league_id) + '/standings'
		
		result = self.api.get_json(endpoint, self.query)
		if not result:
			return None

		return Standings().from_json(result)



class EventsQuery(object):
	def __init__(self, api):
		self.api = api
		self.query = {}


	def load(self):
		done = False
		while not done:
			result = self.api.get_json('events', self.query)
			if not result:
				raise StopIteration
			
			count = result['metadata']['count']
			offset = result['metadata']['offset']
			limit = result['metadata']['limit']

			done = count == 0 
			if not done:
				for ev in result.get('events',[]):
					yield Event().from_json(ev)
				self.query['offset'] = offset + count
			done = count < limit
	

	def fromdate(self, d):
		self.query['fromDate'] = d
		return self

	
	def todate(self, d):
		self.query['toDate'] = d
		return self


	def today(self):
		today = datetime.date.today()
		self.query['toDate'] = self.query['fromDate'] = today.strftime('%Y-%m-%d')
		return self 


	def upcoming(self):
		if 'status' in self.query:
			self.query['status'] += ",UPCOMING"
		else:
			self.query['status'] = "UPCOMING"
		return self

	def finished(self):
		if 'status' in self.query:
			self.query['status'] += ",FINISHED"
		else:
			self.query['status'] = "FINISHED"
		return self


	def leagues(self, *leagues):
		self.query['league'] = ",".join(map(str, leagues))
		return self


	def sport(self, *sports):
		self.query['sport'] = ",".join(map(str, sports))
		return self

	def teams(self, *teams):
		self.query['team'] = ",".join(map(str,teams))
		return self


