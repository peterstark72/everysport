#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''league.py


'''

import api
from commons import Sport, Date
import datetime

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
        self.sport = sport
        self.team_class=team_class
        self._start_date=start_date
        self._end_date=end_date

    @classmethod
    def from_dict(cls, api_client, data):
        '''Creates a League object from a dictionary'''
        return cls(
            api_client,
            data.get('id', None),
            data.get('name', None),
            Sport.from_dict(data.get('sport', {})),
            data.get('teamClass',None), 
            data.get('startDate',None),
            data.get('endDate',None))

    @classmethod        
    def find(cls, api_client, league_id):
        '''Finds the League with the id'''
        endpoint = 'leagues/' + str(league_id)
        data = api_client._fetchresource(endpoint)
        return cls.from_dict(api_client, data.get('league', {}))

    @property
    def start_date(self):
        if self._start_date:
            return Date.from_str(self._start_date)

    @property        
    def end_date(self):
        if self._end_date:
            return Date.from_str(self._end_date)

    @property
    def name(self):
        if self._name:
            return self._name.encode('utf-8') 

    def standings(self):
        return api.StandingsQuery(self.api_client, self.id)

    def events(self):
        return self.api_client.events().leagues(self.id)

    def teamlist(self):
        return [standing.team for standing in self.standings()]

    def rounds(self):
        return {e.round for e in self.events().finished()}

    def grouplabels(self):
        '''Returns a Set of group labels for this league'''
        return {label for standing in self.standings() for label in standing.groups}

    def is_active(self):
        today = datetime.date.today()
        return today > self._league.start_date and today < self._league.end_date




