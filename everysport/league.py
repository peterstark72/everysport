#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''league.py



'''

import datetime

from collections import namedtuple

from edate import Date
from standings import Standings
from season import Season


Sport = namedtuple('Sport', "id name")


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


    def __str__(self):
        return u"{} ({}) {} {}".format(self.name, self.id, self.season.timeuntilend(), self.sport.name).encode('utf-8')


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

    @property
    def standings(self):
        '''Returns Standings for this league'''
        return Standings.find(self.api_client, self.id)

    @property
    def events(self):
        '''Returns EventsQuery for this league'''
        return self.api_client.events().leagues(self.id)

    
    def is_men(self):
        '''Returns True if the teamClass is MEN'''
        return self.team_class == "MEN"

    def teamlist(self):
        '''Returns the list of teams for this league'''
        return [standing.team for standing in self.standings()]

    def rounds(self):
        '''Returna a list of the rounds for which at least one event has finished''' 
        return {e.round for e in self.events().finished()}







