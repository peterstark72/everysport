#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''event.py


'''

from collections import namedtuple

from league import League
from team import Team
from edate import Date


class Arena(namedtuple('Arena', "id name")):
    '''
    Properties:
    name - e.g. "Malmö Arena"
    id - Arena ID

    '''
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            data.get('name', None)
        )

    def __str__(self):
        return self.name.encode('utf-8')

    def __eq__(self, other):
        return self.id == other.id    


class Facts(namedtuple('Facts', "arena, spectators, referees, shots")):
    '''Facts about an event. 

    Properties:
    arena - an Everysport Arena object
    referees - lista of referee names
    shots - 
    spectators - number of spectators at the event

    '''
    __slots__ = ()
    @classmethod
    def from_dict(cls, data):
        return cls(
            Arena.from_dict(data.get('arena', {})),
            data.get('spectators', None),
            data.get('referees', []), #list of names
            data.get('shots', None),
        )



class Event(object):
    '''Everysport Event'''

    def __init__(self, 
            api_client=None,
            id=None,
            start_date=None,
            round_=None,
            status=None,
            hometeam=None,
            visitingteam=None,
            hometeam_score=None,
            visitingteam_score=None,
            finished_time_status=None,
            league=None,
            facts=None):
        self.api_client=api_client
        self.id=id
        self._start_date=start_date
        self.round=round_
        self._hometeam=hometeam
        self._visitingteam=visitingteam
        self.hometeam_score=hometeam_score
        self.visitingteam_score=visitingteam_score
        self.finished_time_status=finished_time_status
        self._league=league
        self._facts=facts

    @classmethod
    def from_dict(cls, api_client, data):
        return cls(
                api_client,
                data.get('id', None),
                data.get('startDate', None),
                data.get('round',None),
                data.get('status',None),
                data.get('homeTeam',{}),
                data.get('visitingTeam',{}),
                data.get('homeTeamScore',None),
                data.get('visitingTeamScore',None),
                data.get('finishedTimeStatus',None),
                data.get('league',{}),
                data.get('facts', {})
            )

    @classmethod
    def find(cls, api_client, event_id):
        endpoint = 'events/' + str(event_id)
        data = api_client._fetchresource(endpoint)
        return cls.from_dict(api_client, data.get('event', {}))

    def __str__(self):
        return u"{:<20} v {:<20} at {} in {}".format(self.hometeam.name, self.visitingteam.name, self.start_date, self.league.name).encode('utf-8')

    @property        
    def start_date(self):
        if self._start_date:
            return Date(self._start_date)

    @property
    def hometeam(self):
        if self._hometeam:
            return Team.from_dict(self._hometeam)

    @property
    def visitingteam(self):
        if self._visitingteam:
            return Team.from_dict(self._visitingteam)

    @property
    def facts(self):
        if self._facts:
            return Facts.from_dict(self._facts)
    
    @property
    def league(self):
        if self._league:
            return League.from_dict(self.api_client, self._league)



