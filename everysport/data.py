#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

The Everysport domain data objects

'''



#Used to parse RFC822 datetime string
from dateutil.parser import parse



class Sport(object):

	def __init__(self, 
		id=None,
		name=None):
		self._id = id
		self._name = name

	def __str__(self):
		return self.name

	@property
	def id(self):
		return self._id


	@property
	def name(self):
		return self._name.encode('utf-8')


	def from_json(self, data):
		return Sport(id=data.get('id', None),
					name=data.get('name', None))

class Arena(object):

	def __init__(self, 
		id=None,
		name=None):
		self._id = id
		self._name = name


	def __str__(self):
		return self.name


	@property
	def id(self):
		return self._id


	@property
	def name(self):
		return self._name.encode('utf-8')

	def from_json(self, data):
		return Arena(id=data.get('id', None),
					name=data.get('name', None))


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

	def __str__(self):
		return self.name.encode('utf-8')

	@property
	def id(self):
		return self._id

	@property
	def link(self):
		return self._link

	@property
	def name(self):
		return self._name

	@property
	def short_name(self):
		return self._short_name


	def from_json(self, data):
		return Team(id=data.get('id', None),
					name=data.get('name', None),
					link=data.get('link', None),
					short_name=data.get('shortName', None))


class Standings(list):
	def get_stats_by_team(self, team_name):
		for standing in self:
			if team_name == standing.team.name:
				return standing.stats	

	def from_json(self, data):
		
		for s in data['groups'][0]['standings']:
			self.append(Standing(
				stats=Stats().from_json(s.get('stats',[])),
				team=Team().from_json(s.get('team', {}))))

		return self


class Standing(object):

	def __init__(self,
			team=None,
			stats=None):
		self._team = team
		self._stats = stats

	def __str__(self):
		return unicode(self.team.name.rjust(20) + str(self.stats).rjust(40)).encode('utf-8')

	@property
	def team(self):
		return self._team	

	@property
	def stats(self):
		return self._stats	


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



	def __str__(self):
		return unicode(self.start_date.strftime('%d/%m %H:%M').ljust(15) + 
						self.home_team.name.ljust(20) + self.visiting_team.name.ljust(20)).encode('utf-8')	

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


		return Event(id=data.get('id', None),
				start_date=data.get('startDate',None),
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


class Stats(object):
	def __init__(self,
			gp=None,
			w=None,
			l=None,
			gf=None,
			ga=None,
			gd=None,
			pts=None):
		self._gp=gp
		self._w=w
		self._l=l
		self._gf=gf
		self._ga=ga
		self._gd=gd
		self._pts=pts

	def __str__(self):
		return "{:5}{:5}{:5}{:5}{:5}{:5}{:10}".format(
						self._gp,
						self._w, 
						self._l,
						self._gf,
						self._ga,
						self._gd,
						self._pts)


	@property
	def gp(self):
		return self._gp

	@gp.setter
	def gp(self, x):
		self._gp = x

	@property
	def w(self):
		return self._w

	@w.setter
	def w(self, x):
		self._w = x


	@property
	def l(self):
		return self._l

	@l.setter
	def l(self, x):
		self._l = x


	@property
	def gf(self):
		return self._gf

	@gf.setter
	def gf(self, x):
		self._gf = x

	@property
	def ga(self):
		return self._ga

	@ga.setter
	def ga(self, x):
		self._ga = x


	@property
	def gd(self):
		return self._gd

	@gd.setter
	def gd(self, x):
		self._gd = x


	@property
	def pts(self):
		return self._pts

	@pts.setter
	def pts(self, x):
		self._pts = x


	def from_json(self, data):
		for d in data:
			self.__setattr__(d['name'], d['value'])
		return self









