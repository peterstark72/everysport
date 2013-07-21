#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Event domain objects

See Everysport API documentation at:
https://github.com/menmo/everysport-api-documentation

'''

import datetime
from collections import namedtuple


from leagues import Team



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


class Facts(namedtuple('Facts', "arena, spectators, referees, shots")):
    __slots__ = ()
    @classmethod
    def from_dict(cls, data):
        return cls(
            Arena.from_dict(data.get('arena', {})),
            data.get('spectators', None),
            data.get('referees', []), #list of names
            data.get('shots', None),
        )


class Event(namedtuple('Event', "id, start_date, time_zone, round, status, home_team, visiting_team, home_team_score, visiting_team_score, finished_time_status, league,facts")):
    __slots__ = ()
    
    @classmethod    
    def from_dict(cls, data):
        try:
            d = data['startDate'][0:16] #Strip timezone
            start_date = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M")
        except:
            start_date = None

        return cls(
                data.get('id', None),
                start_date,
                "CEST", #All events today are in CEST timezone
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







