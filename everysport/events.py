#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''events.py


'''

import datetime
from collections import namedtuple


from teams import Team as Team
from resource import getresource as getresource


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

    STATUS_FINISHED = "FINISHED"

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


    @classmethod    
    def from_resource(cls, url):

        data = getresource(url)     

        return cls.from_dict(data.get('event', {}))


    def is_finished(self):
        return self.status == Event.STATUS_FINISHED






class EventsList(list):
    '''A list of events returned from the API'''
    @classmethod
    def from_resource(cls, url):

        data = getresource(url)

        obj = cls.__new__(cls)

        for ev in data.get('events',[]):
            obj.append(Event.from_dict(ev))

        obj.credit = Credit.from_dict(data.get('credit', {}))
        
        obj.offset = data['metadata']['offset']
        obj.limit = data['metadata']['limit']
        obj.count = data['metadata']['count']

        return obj 
