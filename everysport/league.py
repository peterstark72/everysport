#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''league.py



'''

import datetime

from collections import namedtuple

from standings import Standings
from season import Season





class Sport(namedtuple('Sport', "id name")):
    '''A tuple with an ID and a name'''
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            data.get('name', None)
        )


    def __repr__(self):
        return "Sport({})".format(",".join(map(repr,[self.name, self.id])))        

    def __eq__(self, other):
        return self.id == other.id  



class League(object):
    '''Everysport League object'''

    def __init__(self, 
        api_client=None,
        id=None,
        name=None,
        sport=None,
        team_class=None,
        start_date=None,
        end_date=None):
        self.api_client=api_client
        self.id = id
        self._name = name
        self._sport = sport
        self.team_class=team_class
        self._start_date = start_date
        self._end_date = end_date
        self._round = "" #Current round

    @classmethod
    def from_dict(cls, api_client, data):
        '''Creates a League object from a dictionary'''
        return cls(
            api_client,
            data.get('id', None),
            data.get('name', None),
            data.get('sport', {}),
            data.get('teamClass',None), 
            data.get('startDate',None),
            data.get('endDate',None))

    @classmethod        
    def find(cls, api_client, league_id):
        '''Finds the League with the id'''
        endpoint = 'leagues/' + str(league_id)
        data = api_client._fetchresource(endpoint)
        return cls.from_dict(api_client, data.get('league', {}))


    def __repr__(self):
        return "League({})".format(",".join(map(repr, [self.name, self.id, self.season, self.sport])))


    def _get_current_round(self):
        return max(self.rounds())


    @property
    def season(self):
        return Season(self._start_date, self._end_date)

    @property
    def name(self):
        if self._name:
            return self._name

    @property
    def sport(self):
        if self._sport:
            return Sport(self._sport.get('id'), self._sport.get('name'))


    def _getstandings(self, round_="", type_="total"):
        return Standings.find(self.api_client, self.id, round_, type_)


    @property 
    def standings(self):
        '''Returns Total Standings for this league'''
        return self.totals 

    @property
    def totals(self):
        '''Returns Total Standings for this league'''
        return self._getstandings(self._round, "total")

    @property
    def home(self):
        '''Returns Home Standings for this league'''
        return self._getstandings(self._round, "home")

    @property
    def away(self):
        '''Returns Away Standings for this league'''
        return self._getstandings(self._round, "away")


    def round(self, r):
        '''Set set the league to a specifc round'''
        self._round = r 
        return self    

    def current(self):
        '''Set set the league to current (latest) round'''
        self._round = ""
        return self  

    @property        
    def events(self):
        '''Returns list of event in the round'''
        if not self._round:
            self.current()
        return self.allevents.round(self._round).fetch()


    @property
    def results(self):
        '''Returns list of results until the current round. If no round is set, you get all finished events until today.'''
        q = self.api_client.events.leagues(self.id)
        if self._round:
            q = q.round(*range(1,self._round+1)).finished()
        else:
            q = q.finished()
        return q.fetch()


    @property 
    def allevents(self):
        '''Returns iterator of all events, in all rounds'''
        return self.api_client.events.leagues(self.id)


    @property
    def teamlist(self):
        '''The list of teams'''
        return [standing.team for standing in self.standings]


    @property
    def roundslist(self):
        '''The list of the rounds for which at least one event has finished''' 
        return {e.round for e in self.allevents.finished()}
