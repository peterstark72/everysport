#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

A simple library that wraps the Everysport API. 


Usage: 

api = Api(EVERYSPORT_APIKEY)

an_event = api.events().get(EVERYSPORT_EVENT_ID)

events = api.events().all()


'''


import datetime
import urllib
import json
import logging

#Used to parse RFC822 datetime string
from dateutil.parser import parse


BASE_API_URL = "http://api.everysport.com/v1/{}"

class EverysportException(Exception):
	pass


class Api(object):
	def __init__(self, apikey):
		self.params = {}
		self.params['apikey'] = apikey

	def events(self):
		"""Returns a query for all events"""
		return EventsQuery(self)

	def leagues(self):
		"""Returns a query for all leagues"""
		return LeaguesQuery()


	def get_json(self, endpoint, params=dict()):
		'''GETs an endpoint or raises an exception'''
		
		self.params.update(params)
		encoded_params = urllib.urlencode(self.params)
		url = BASE_API_URL.format(endpoint) + '?' + encoded_params	


		try:			
			response = urllib.urlopen(url)
			result = json.load(response)
		except:
			raise EverysportException("Could not load {}".format(url))
		
		return result 




class Query(object):
	def __init__(self, api):
		self.api = api
		self.query = {}


	def get(self, resource, resource_id):

		endpoint = "{}s/{}".format(repr(resource), str(resource_id))

		try:
			result = self.api.get_json(endpoint, self.query)
		except EverysportException as e:
			logging.warning(e.message)
			return None

		event_json = result.get(repr(resource),{})

		return resource().from_json(event_json)



	def all(self, resource):

		endpoint = repr(resource)+"s"

		done = False
		while not done:
			try:	
				result = self.api.get_json(endpoint, self.query)
			except EverysportException as e:
				logging.warning(e.message)
				raise StopIteration
			
			count = result['metadata']['count']
			offset = result['metadata']['offset']
			limit = result['metadata']['limit']

			done = count == 0 
			if not done:
				for ev in result.get(endpoint,[]):
					yield resource.from_json(ev)
				self.query['offset'] = offset + count
			done = count < limit		



class LeaguesQuery(Query):

	def team_class(self, *team_classes):
		self.query['teamClass'] = ",".join(map(str, team_classes))
		return self


	def sport(self, *sports):
		self.query['sport'] = ",".join(map(str, sports))
		return self


	def all(self):
		return super(LeaguesQuery, self).all(League())




class EventsQuery(Query):

	def get(self, event_id):
		return super(EventsQuery, self).get(Event(), event_id)

	def all(self):
		return super(EventsQuery, self).all(Event())
	

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




class Team(object):

	def __init__(self, 
		id=None,
		link=None,
		name=None,
		short_name=None):
		self._id = id
		self._link = link
		self._name = name
		self._short_name = short_name


	@property
	def id(self):
		return self._id

	@property
	def link(self):
		return self._link

	@property
	def name(self):
		return self._name.encode('utf-8')

	@property
	def short_name(self):
		return self._short_name


	def from_json(self, data):
		return Team(id=data.get('id', None),
					name=data.get('name', None),
					link=data.get('link', None),
					short_name=data.get('shortName', None))



class Sport(object):

	def __init__(self, 
		id=None,
		name=None):
		self._id = id
		self._name = name


	@property
	def id(self):
		return self._id


	@property
	def name(self):
		return self._name


	def from_json(self, data):
		return Sport(id=data.get('id', None),
					name=data.get('name', None))

class Arena(object):

	def __init__(self, 
		id=None,
		name=None):
		self._id = id
		self._name = name


	@property
	def id(self):
		return self._id


	@property
	def name(self):
		return self._name

	def from_json(self, data):
		return Arena(id=data.get('id', None),
					name=data.get('name', None))

class League(object):

	def __init__(self, 
		id=None,
		name=None,
		sport=None,
		team_class=None):
		self._id = id
		self._name = name
		self._sport = sport
		self._team_class = team_class


	def __repr__(self):
		return 'league'

	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name.encode('utf-8')

	@property
	def sport(self):
		return self._sport

	@property
	def team_class(self):
		return self._team_class

	def from_json(self, data):
		if 'sport' in data: 
			sport = Sport().from_json(data['sport'])
		else: 
			sport = None
		return League(id=data.get('id', None),
					name=data.get('name', None),
					sport=sport,
					team_class=data.get('teamClass',None))




class Event(object):

	def __init__(self, 
		id=None,
		start_date=None,
		round=None,
		status=None,
		home_team=None,
		visiting_team=None,
		home_team_score=None,
		visiting_team_score=None,
		league=None,
		arena=None,
		spectators=None,
		referees=None):
		self._id = id
		self._start_date = start_date
		self._round = round
		self._status = status
		self._home_team = home_team
		self._visiting_team = visiting_team
		self._home_team_score=home_team_score
		self._visiting_team_score=visiting_team_score
		self._league = league
		self._arena=arena	
		self._spectators=spectators
		self._referees=referees


	def __repr__(self):
		return 'event'
	


	def __str__(self):
		return "{} : {} - {}".format(self.start_date.strftime('%d/%m %H:%M'),
						self.home_team.name, 
						self.visiting_team.name)	

	@property
	def id(self):
		return self._id


	@property
	def start_date(self):
		return parse(self._start_date)

	@property
	def round(self):
		return self._round


	@property
	def status(self):
		'''The status of the event'''
		return self._status

	@property
	def home_team(self):
		return self._home_team


	@property
	def visiting_team(self):
		return self._visiting_team

	@property
	def home_team_score(self):
		return self._home_team_score

	@property
	def visiting_team_score(self):
		return self._visiting_team_score


	@property
	def league(self):
		return self._league


	@property
	def arena(self):
		return self._arena

	@property
	def spectators(self):
		return self._spectators

	@property
	def referees(self):
		return self._referees



	def from_json(self, data):

		if 'homeTeam' in data:			
			home_team = Team().from_json(data['homeTeam'])
		else:
			home_team = None

		if 'visitingTeam' in data:	
			visiting_team = Team().from_json(data['visitingTeam'])
		else:
			visiting_team = None
		
		if 'league' in data:
			league = League().from_json(data['league'])	
		else:
			league = None


		if 'facts' in data:
			if 'arena' in data['facts']:
				arena = Arena().from_json(data['facts']['arena'])
			else:
				arena = None
			spectators = data['facts'].get('spectators', None)
			referees = data['facts'].get('referees', None)
		else:
			arena = None
			spectators = None
			referees = None


		return Event(start_date=data.get('startDate',None),
				status=data.get('status',None),
				round=data.get('round',None),
				home_team=home_team,
				visiting_team=visiting_team,
				home_team_score=data.get('homeTeamScore',None),
				visiting_team_score=data.get('visitingTeamScore',None),
				league=league,
				arena=arena,
				spectators=spectators,
				referees=referees
			)

