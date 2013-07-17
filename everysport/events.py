#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Event domain objects

See Everysport API documentation at:
https://github.com/menmo/everysport-api-documentation

'''

import datetime
from collections import namedtuple


from teams import Team as Team
from resource import getresource as getresource

import url_builder


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


EventResult = namedtuple('EventResul', "gf, ga, against")
    

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
    def from_url(cls, url):

        data = getresource(url)     

        return cls.from_dict(data.get('event', {}))


    def is_finished(self):
        return self.status == Event.STATUS_FINISHED





class EventsIterator(object):
    '''A list of events returned from the API'''
    
    def __init__(self, query):
        self.query = query


    def __iter__(self):
        '''Generator over events.'''

        done = False
        while not done:
            
            url = url_builder.get_events_url(*self.query.league_ids, **self.query.params)
            try:
                data = getresource(url)                    
                result = data.get('events', [])
                offset = data['metadata']['offset']
                limit = data['metadata']['limit']
                count = data['metadata']['count']
            except:
                raise StopIteration
            
            done = count == 0 
            if not done:
                for ev in result:
                    yield Event.from_dict(ev)
                self.query.params['offset'] = offset + count
            done = count < limit    


 

class EventsList(list):
    '''A list of events'''
    def __init__(self, events):
        for ev in events:
            self.append(ev)

    def get_events_for_team(self, team_id):
        '''Returns the list of events where the team takes part''' 
        return EventsList([e for e in self if team_id in (e.home_team.id, e.visiting_team.id)])


    def groupby(self, grouper):
        '''Returns a dictionary with groups of events, set by grouper.'''
        groups = {}
        for e in self:
            groups.setdefault(getattr(e,grouper), []).append(e)
        return groups
    













