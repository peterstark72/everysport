#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

A simple library that wraps the Everysport API. 


'''


import datetime
import urllib
import urllib2
import json
import logging

from data import Event
from data import Groups


BASE_API_URL = "http://api.everysport.com/v1/{}"


class Api(object):
	def __init__(self, apikey):
		self._apikey = apikey


	def events(self):
		'''Returns a Query object for events'''
		return EventsQuery(self)


	def standings(self):
		'''Returns a Query object for standings'''
		return StandingsQuery(self)


	def get_json(self, endpoint, params=dict()):
		'''Called by the query object to get a resource from the Api'''
		params['apikey'] = self._apikey
		
		encoded_params = urllib.urlencode(params)
		url = BASE_API_URL.format(endpoint) + '?' + encoded_params	

		try:	
			response = urllib2.urlopen(url)
			result = json.load(response)	
		except urllib2.HTTPError as e:
			logging.warning("Could not load {}. HTTP code: {}".format(url, e.code))
			return None

		return result



class StandingsQuery(object):
	def __init__(self, api):
		self.api = api
		self.query = {}

	def total(self):
		'''Queries for Total standings '''
		self.query['type'] = 'total'
		return self

	def home(self):
		'''Queries for Home standings '''
		self.query['type'] = 'home'
		return self		

	def away(self):
		'''Queries for Away standings '''
		self.query['type'] = 'away'
		return self		

	def round(self, x):
		'''Queries for a specific round '''
		self.query['round'] = x
		return self	

	def get(self, league_id):
		'''Loads the standings from the API and returns a Standings object'''
		endpoint = 'leagues/' + str(league_id) + '/standings'
		
		result = self.api.get_json(endpoint, self.query)

		if result:
			return Groups(result)
		else: 
			return Groups()



class EventsQuery(object):
	def __init__(self, api):
		self.api = api
		self.query = {}

	def get(self, event_id):
		'''Get one event from the API. Returns an Event object or None'''
		endpoint = 'events/' + str(event_id)
		
		result = self.api.get_json(endpoint)
		
		if result:
			return Event.from_json(result.get('event',{}))
		else:
			return None	


	def get_all(self, *leagues):
		'''Generator that loads all events from the API.'''

		if len(leagues)>0:
			self.query['league'] = ",".join(map(str, leagues))

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
					yield Event.from_json(ev)
				self.query['offset'] = offset + count
			done = count < limit
	

	def fromdate(self, d):
		'''Queries events from this date'''
		self.query['fromDate'] = d
		return self

	
	def todate(self, d):
		'''Queries events to this date'''
		self.query['toDate'] = d
		return self


	def today(self):
		'''Queries today's events'''
		today = datetime.date.today()
		self.query['toDate'] = self.query['fromDate'] = today.strftime('%Y-%m-%d')
		return self 


	def upcoming(self):
		'''Queries for all upcoming events'''
		self.query['status'] = "UPCOMING"
		return self

	def finished(self):
		'''Queries for all finished events'''
		self.query['status'] = "FINISHED"
		return self

	def sport(self, *sports):
		'''Queries events for one or many sports, by Sport ID'''
		self.query['sport'] = ",".join(map(str, sports))
		return self

	def teams(self, *teams):
		'''Queries events for one or many teams, by Team ID'''
		self.query['team'] = ",".join(map(str,teams))
		return self


