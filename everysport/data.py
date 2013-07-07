#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

The Everysport domain data objects

'''

import json
from dateutil.parser import parse
from collections import namedtuple



class Team(namedtuple('Team', "id, name, short_name, abbreviation")):
	__slots__ = () #prevent creation of instance dict
	@classmethod
	def from_dict(cls, data):
		return cls(
			data.get('id', None),
			data.get('name', None),
			data.get('short_name', None),
			data.get('abbreviation', None)
		)


class Sport(namedtuple('Sport', "id, name")):
	__slots__ = () 
	@classmethod
	def from_dict(cls, data):
		return cls(
			data.get('id', None),
			data.get('name', None)
		)


class Arena(namedtuple('Arena', "id, name")):
	__slots__ = () 
	@classmethod
	def from_dict(cls, data):
		return cls(
			data.get('id', None),
			data.get('name', None)
		)


class Label(namedtuple('Label', "name, type")):
	__slots__ = () 
	@classmethod
	def from_dict(cls, data):
		return cls(
			data.get('name', None),
			data.get('type', None)
		)


class Credit(namedtuple('Credit', "message, link, logoUrl")):
	__slots__ = () 
	@classmethod
	def from_dict(cls, data):
		return cls(
			data.get('message', None),
			data.get('link', None),
			data.get('logoUrl', None)
		)


class League(namedtuple('League', "id, name, sport, team_class")):
	__slots__ = () 
	@classmethod
	def from_dict(cls, data):
		return cls(
			data.get('id', None),
			data.get('name', None),
			Sport.from_dict(data.get('sport', {})),
			data.get('team_class', None),
		)



class Facts(namedtuple('Facts', "arena,spectators,referees,shots")):
	__slots__ = ()
	@classmethod
	def from_dict(cls, data):
		return cls(
			Arena.from_dict(data.get('arena', {})),
			data.get('spectators', None),
			data.get('referees', []), #list of names
			data.get('shots', None),
		)



class Event(namedtuple('Event', "id, start_date, round, status, home_team, visiting_team, home_team_score, visiting_team_score, finished_time_status, league,facts")):
	__slots__ = ()

	STATUS_FINISHED = "FINISHED"

	@classmethod	
	def from_dict(cls, data):
		return cls(
				data.get('id', None),
				parse(data.get('startDate',None)), #Date is RFC822
				data.get('round',None),
				data.get('status',None),
				Team.from_dict(data.get('homeTeam',{})),
				Team.from_dict(data.get('visitingTeam',{})),
				data.get('homeTeamScore',None),
				data.get('visitingTeamScore',None),
				data.get('finishedTimeStatus',None),
				League.from_dict(data.get('league',{})),
				Facts.from_dict(data.get('facts', {}))
			)


	@classmethod	
	def from_json(cls, json_doc):
		data = json.load(json_doc)			
		return cls.from_dict(data.get('event', {}))


	def is_finished(self):
		return self.status == Event.STATUS_FINISHED



class Stats(object):	
	@classmethod	
	def from_list(cls, data):
		'''We get this as list of name/value pairs from the API'''
		
		obj = cls.__new__(cls)
		
		for stat in data:
			setattr(obj,stat['name'],stat['value'])
		
		return obj



class TeamStandings(namedtuple('TeamStandings', "team, stats")):
	__slots__ = ()
	@classmethod	
	def from_dict(cls, data):
		return cls(
			Team.from_dict(data.get('team', {})),
			Stats.from_list(data.get('stats',[]))
			)



class StandingsGroup(namedtuple('StandingsGroup', "labels, standings")):
	__slots__ = ()
	@classmethod	
	def from_dict(cls, data):

		labels = []
		for lbl in data.get('labels', []):
			labels.append(Label.from_dict(lbl))


		standings = []
		for sta in data.get('standings', []):
			standings.append(TeamStandings.from_dict(sta))
			
		return cls(labels, standings)



'''

Resources 

'''
class Events(list):
	@classmethod	
	def from_json(cls, json_doc):

		data = json.load(json_doc)			

		obj = cls.__new__(cls)

		for ev in data.get('events',[]):
			obj.append(Event.from_dict(ev))

		obj.credit = Credit.from_dict(data.get('credit', {}))
		
		obj.offset = data['metadata']['offset']
		obj.limit = data['metadata']['limit']
		obj.count = data['metadata']['count']

		return obj



class Standings(list):
	@classmethod
	def from_json(cls, json_doc):
		
		data = json.load(json_doc)

		obj = cls.__new__(cls)

		for group in data.get('groups', []):
			obj.append(StandingsGroup.from_dict(group))
		
		obj.credit = Credit.from_dict(data.get('credit', {}))

		return obj

