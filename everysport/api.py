#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

A simple library that wraps the Everysport API. 


'''


import datetime
import urllib
import urllib2

from data import Event, Events, Standings


BASE_API_URL = "http://api.everysport.com/v1/{}"


class EverysportException(Exception):
	pass


class Api(object):
	def __init__(self, apikey):
		self.apikey = apikey

	def events(self):
		'''Returns a Query object for events'''
		return EventsQuery(self.apikey)


	def standings(self):
		'''Returns a Query object for standings'''
		return StandingsQuery(self.apikey)



class UrlBuilder(object):
	'''Builder for URLs for various endpoints'''
	def __init__(self):
		self.url = ""

	def standings(self, league_id):
		endpoint = 'leagues/' + str(league_id) + '/standings'
		self.url = BASE_API_URL.format(endpoint)
		return self

	def events(self):
		endpoint = 'events'
		self.url = BASE_API_URL.format(endpoint)
		return self

	def event(self, event_id):
		endpoint = 'events/' + str(event_id) 
		self.url = BASE_API_URL.format(endpoint)
		return self

	def with_params(self, params_dict):
		encoded_params = urllib.urlencode(params_dict)
		self.url += "?" + encoded_params 
		return self	

	def get(self):
		'''Send a GET request to the URL'''
		return urllib2.urlopen(self.url)
 


class ApiQuery(object):
	'''Base class for all queries. '''
	def __init__(self, apikey):
		'''Initialized with the API and empty query '''
		self.params = {}
		self.params['apikey'] = apikey


class StandingsQuery(ApiQuery):
	'''A Query for a league's standings (tables). In most leagues, just one. But e.g. NHL have many groups.

		It returns a Standings object which contains a list of StandingGroups. Each group contains a list of labels and the actual standings for the group. The standings contains the team and a list of team stats. 

	
		Arguments:
			type - one of 'total' (default), 'home' and 'away'
			round - specifies standings after a specific round, eg. '10'. Default is the last played round.
	'''		

	def total(self):
		'''Queries for Total standings '''
		self.params['type'] = 'total'
		return self

	def home(self):
		'''Queries for Home standings '''
		self.params['type'] = 'home'
		return self		

	def away(self):
		'''Queries for Away standings '''
		self.params['type'] = 'away'
		return self		

	def round(self, x):
		'''Queries for a specific round '''
		self.params['round'] = x
		return self	

	def league(self, league_id):
		self.league_id = league_id
		return self

	def load(self):
		'''Loads all groups of standings for this league.'''
		
		url = UrlBuilder().standings(self.league_id).with_params(self.params)
		try: 
			response = url.get()
			result = Standings.from_json(response)
		except:
			raise EverysportException("Could not load {}".format(url))

		return result




class EventsQuery(ApiQuery):
	'''A query for one or many events. 

		Arguments:
		league - list of league IDs, for which to retrieve events.
		upcoming - gets upcoming games
		finisged - gets finisged games 
		fromDate - filters out events after a specific date
		toDate - filters out events before a specific date
		round - one or many rounds, for which to retrieve events.
		team - one or many team IDs, for which to retrieve events.
		sport - one or many sport IDs, for which to retrieve events.

	'''

	def fromdate(self, d):
		'''Queries events from this date'''
		self.params['fromDate'] = d
		return self

	
	def todate(self, d):
		'''Queries events to this date'''
		self.params['toDate'] = d
		return self


	def today(self):
		'''Queries today's events'''
		today = datetime.date.today()
		self.params['toDate'] = self.params['fromDate'] = today.strftime('%Y-%m-%d')
		return self 


	def upcoming(self):
		'''Queries for all upcoming events'''
		self.params['status'] = "UPCOMING"
		return self

	def finished(self):
		'''Queries for all finished events'''
		self.params['status'] = "FINISHED"
		return self

	def sport(self, *sports):
		'''Queries events for one or many sports, by Sport ID'''
		self.params['sport'] = ",".join(map(str, sports))
		return self

	def teams(self, *teams):
		'''Queries events for one or many teams, by Team ID'''
		self.params['team'] = ",".join(map(str,teams))
		return self

	def round(self, *x):
		'''Queries for a specific round '''
		self.params['round'] = ",".join(map(str,x))
		return self	

	def leagues(self, *leagues):
		'''Queries for one or many leagues'''
		self.params['league'] = ",".join(map(str, leagues))
		return self		


	def load(self, event_id):
		'''Get one event from the API. Returns an Event object or raises EverysportExceptions'''
		
		url = UrlBuilder().event(event_id).with_params(self.params)
		try:
			response  = url.get()
		except:
			raise EverysportException('Could not load {}'.format(url))

		return Event.from_json(response)


	def __iter__(self):
		'''Generator that loads all events from the API.'''

		done = False
		while not done:
			
			url = UrlBuilder().events().with_params(self.params)
			try:
				response = url.get()
				result = Events.from_json(response)
			except:
				raise StopIteration
			
			done = result.count == 0 
			if not done:
				for ev in result:
					yield ev
				self.params['offset'] = result.offset + result.count
			done = result.count < result.limit







