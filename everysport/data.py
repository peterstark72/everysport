#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

The Everysport domain data objects

'''


from dateutil.parser import parse



class DataObject(object):

	#The base DataObject has no properties 
	_properties = []
	
	def __init__(self, *args):
		'''Normal initialization from argument list'''

		if len(args) != len (self._properties):
			raise TypeError('Expected {} arguments'.format(len(self._properties)))

		#Set arguments
		for name, value in zip(self._properties, args):
			setattr(self, name, value)	


	@classmethod	
	def from_json(cls, json_obj):
		'''Unpack JSON object'''
		obj = cls.__new__(cls)
		
		for name, value in json_obj.items():
			setattr(obj,name,value)
		
		return obj



class Sport(DataObject):
	_properties = ['id', 'name']


class Arena(DataObject):
	_properties = ['id', 'name']


class Team(DataObject):
	_properties = ['id', 'name', 'link','short_name','abbreviation']



class Stats(DataObject):
	_properties = ['gp', 'w', 'ow','l','ol','gf','ga','gd','pts']

	@classmethod	
	def from_json(cls, json_array):
		'''Creates a data object from JSON array '''
		
		obj = cls.__new__(cls)
		
		for stat in json_array:
			setattr(obj,stat['name'],stat['value'])
		
		return obj


	def __str__(self):
		return "{:5}{:5}{:5}{:5}{:5}{:5}{:10}".format(
						self.gp,
						self.w, 
						self.l,
						self.gf,
						self.ga,
						self.gd,
						self.pts)


class Label(DataObject):
	_properties = ['name', 'type']
	def __str__(self):
		return "{} ({})".format(unicode(self.name), self.type)


class LabelsList(list):
	def __init__(self, data):
		for d in data:
			self.append(Label(d.get('name'), d.get('type')))


class Standing(DataObject):
	_properties = ['team', 'stats']

	@classmethod
	def from_json(cls, json_obj):
		return cls(
			Team.from_json(json_obj.get('team', {})),
			Stats.from_json(json_obj.get('stats', []))
			)

	def __str__(self):
		return unicode(self.team.name.rjust(20) + str(self.stats).rjust(40)).encode('utf-8')



class StandingsList(list):
	def __init__(self, data):
		for s in data:
			self.append(Standing.from_json(s))


class StandingGroup(DataObject):
	_properties = ['labels', 'standings']


class StandingGroupList(list):
	def __init__(self, data):
		for group in data.get('groups',[]):
			self.append(StandingGroup(
				LabelsList(group.get('labels',[])),
				StandingsList(group.get('standings', []))
				)
			)


class League(DataObject):
	_properties = ['id', 'name', 'sport', 'team_class']

	@classmethod
	def from_json(cls, json_obj):
		return cls(json_obj.get('id', None),
					json_obj.get('name', None),
					Sport.from_json(json_obj.get('sport', {})),
					json_obj.get('teamClass',None))


class Facts(DataObject):
	_properties = ['arena','spectators','referees','shots']

	@classmethod
	def from_json(cls, json_obj):
		return cls(
			Arena.from_json(json_obj.get('arena',{})),
			json_obj.get('spectators',None),
			json_obj.get('referees', []),
			json_obj.get('shots', None)
			)



class Event(DataObject):
	_properties = ['id', 'start_date', 'round', 'status', 'home_team','visiting_team', 'home_team_score','visiting_team_score','finished_time_status','league','facts']

	STATUS_FINISHED = "FINISHED"
	STATUS_UPCOMING = "UPCOMING"
	STATUS_PENDING = "PENDING"

	def is_finished(self):
		return self.status == Event.STATUS_FINISHED


	@classmethod	
	def from_json(cls, json_obj):
		return cls(
				json_obj.get('id', None),
				parse(json_obj.get('startDate',None)), #Date is RFC822
				json_obj.get('round',None),
				json_obj.get('status',None),
				Team.from_json(json_obj.get('homeTeam',{})),
				Team.from_json(json_obj.get('visitingTeam',{})),
				json_obj.get('homeTeamScore',None),
				json_obj.get('visitingTeamScore',None),
				json_obj.get('finishedTimeStatus',None),
				League.from_json(json_obj.get('league',{})),
				Facts.from_json(json_obj.get('facts', {}))
			)


	def __str__(self):
		s = ""
		if self.is_finished():
			s += self.start_date.strftime("%d/%m %H:%M").ljust(15) + self.home_team.name.ljust(20) + str(self.home_team_score).ljust(5) + " " +self.visiting_team.name.ljust(20) + str(self.visiting_team_score).ljust(5)
		else:
			s += self.start_date.strftime("%d/%m %H:%M").ljust(15) + self.home_team.name.ljust(20)  +self.visiting_team.name.ljust(20)

		if len(self.shots) > 0:
			s += "\n" + self.shots

		return s.encode('utf-8')	














