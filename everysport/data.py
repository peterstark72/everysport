#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

The Everysport domain data objects

'''



#Used to parse RFC822 datetime string
from dateutil.parser import parse


class DataObject(object):
	_properties = []
	def __init__(self, *args):

		if len(args) != len (self._properties):
			raise TypeError('Expected {} arguments'.format(len(self._properties)))

		#Set arguments
		for name, value in zip(self._properties, args):
			setattr(self, name, value)	

	@classmethod	
	def from_json(cls, data):
		obj = cls.__new__(cls)
		for name, value in data.items():
			setattr(obj,name,value)
		return obj



class Sport(DataObject):
	_properties = ['id', 'name']


class Arena(DataObject):
	_properties = ['id', 'name']


class Stats(DataObject):
	_properties = ['gp', 'w', 'l','gf','ga','gd','pts']
	def __str__(self):
		return "{:5}{:5}{:5}{:5}{:5}{:5}{:10}".format(
						self.gp,
						self.w, 
						self.l,
						self.gf,
						self.ga,
						self.gd,
						self.pts)

	@classmethod	
	def from_json(cls, data):
		obj = cls.__new__(cls)
		for stat in data:
			setattr(obj,stat['name'],stat['value'])
		return obj


class Team(DataObject):
	_properties = ['id', 'name', 'link','short_name']


class Label(DataObject):
	_properties = ['name', 'type']
	def __str__(self):
		return "{} ({})".format(unicode(self.name), self.type)


class Labels(list):
	def __init__(self, data):
		for d in data:
			self.append(Label(d.get('name'), d.get('type')))


class Standing(DataObject):
	_properties = ['team', 'stats']
	def __str__(self):
		return unicode(self.team.name.rjust(20) + str(self.stats).rjust(40)).encode('utf-8')

	@classmethod
	def from_json(cls, data):
		return cls(
			Team.from_json(data.get('team', {})),
			Stats.from_json(data.get('stats', []))
			)


class Standings(list):
	def __init__(self, data):
		for s in data:
			self.append(Standing.from_json(s))


class Group(DataObject):
	_properties = ['labels', 'standings']


class Groups(list):
	def __init__(self, data):
		for group in data.get('groups',[]):
			self.append(Group(
				Labels(group.get('labels',[])),
				Standings(group.get('standings', []))
				)
			)


class League(DataObject):
	_properties = ['id', 'name', 'sport', 'team_class']


	@classmethod
	def from_json(cls, data):
		if 'sport' in data: 
			sport = Sport.from_json(data['sport'])
		else: 
			sport = None

		return cls(data.get('id', None),
					data.get('name', None),
					sport,
					data.get('teamClass',None))



class Event(DataObject):
	_properties = ['id', 'start_date', 'round', 'status', 'home_team','visiting_team', 'home_team_score','visiting_team_score','league','arena','spectators','referees']

	STATUS_FINISHED = "FINISHED"
	STATUS_UPCOMING = "UPCOMING"
	STATUS_PENDING = "PENDING"

	def __str__(self):

		if self.is_finished():
			return unicode(self.start_date.strftime("%d/%m %H:%M").ljust(15) + self.home_team.name.ljust(20) + str(self.home_team_score).ljust(5) + " " +self.visiting_team.name.ljust(20) + str(self.visiting_team_score).ljust(5)).encode('utf-8')
		else:
			return unicode(self.start_date.strftime("%d/%m %H:%M").ljust(15) + self.home_team.name.ljust(20)  +self.visiting_team.name.ljust(20)).encode('utf-8')



	def is_finished(self):
		return self.status == Event.STATUS_FINISHED


	@classmethod	
	def from_json(cls, data):

		if 'homeTeam' in data:			
			home_team = Team.from_json(data['homeTeam'])
		else:
			home_team = None

		if 'visitingTeam' in data:	
			visiting_team = Team.from_json(data['visitingTeam'])
		else:
			visiting_team = None
		
		if 'league' in data:
			league = League.from_json(data['league'])	
		else:
			league = None


		if 'facts' in data:
			if 'arena' in data['facts']:
				arena = Arena.from_json(data['facts']['arena'])
			else:
				arena = None
			spectators = data['facts'].get('spectators', None)
			referees = data['facts'].get('referees', None)
		else:
			arena = None
			spectators = None
			referees = None


		return cls(data.get('id', None),
				parse(data.get('startDate',None)),				
				data.get('round',None),
				data.get('status',None),
				home_team,
				visiting_team,
				data.get('homeTeamScore',None),
				data.get('visitingTeamScore',None),
				league,
				arena,
				spectators,
				referees
			)














