#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''api.py


'''

import urllib
import urllib2
import datetime
import logging
import hashlib
import json


from league import League
from event import Event
from commons import Standing


BASE_API_URL = "http://api.everysport.com/v1/{}"


class EverysportException(Exception):
    '''Exception for the Everysport module'''
    pass


class Api(object):
    '''A Python wrapper for the Everysport API

    Example usage: 

    api = everysport.Api(APIKEY)
    nhl = api.league(everysport.NHL)
    hockey_leagues = api.leagues().sport(2)

    '''

    _cache = {}

    def __init__(self, apikey):
        self.apikey = apikey  

    def league(self, league_id):
        '''Returns a League object '''
        return League.find(self, league_id)   

    def event(self, event_id):
        '''Returns an Event object'''
        return Event.find(self, event_id)

    def leagues(self):
        '''Returns LeaguesQuery'''
        return LeaguesQuery(self)

    def events(self):
        '''Returns EventsQuery'''
        return EventsQuery(self)


    def _fetchresource(self, endpoint, **params):
        '''Sends the Query and returns the response''' 

        url = BASE_API_URL.format(endpoint) + "?apikey=" + self.apikey

        if params:
            url += "&" + urllib.urlencode(params)


        #Check if already in cache, else add it
        key = hashlib.md5(url).hexdigest()
        if key not in self._cache:
            try:
                logging.debug("fetching {}".format(url))
                response = urllib2.urlopen(url)
                self._cache[key] = json.load(response)
            except Exception as e:
                raise EverysportException('Could not load {} with {} : \n{}'.format(url, params, e.message))

        return self._cache[key]


    def _fetchpages(self, endpoint, entity_name, entity_func, **params):

        done = False
        while not done:
            try:
                data = self._fetchresource(endpoint, **params)                    
                page = data.get(entity_name, [])

                offset = data['metadata']['offset']
                limit = data['metadata']['limit']
                count = data['metadata']['count']
            except:
                raise StopIteration
            
            done = count == 0 
            if not done:
                for entity in page:
                    yield entity_func(self, entity)
                params['offset'] = offset + count
            done = count < limit 



class ApiQuery(object):
    '''Abstract object for Queries against the API'''

    def __init__(self, api_client):
        self.api_client  = api_client
        self.params = {}


class LeaguesQuery(ApiQuery):
    '''Query for leagues'''

    def sport(self, *sports):
        '''Queries events for one or many sports, by Sport ID'''
        self.params['sport'] = ",".join(map(str, sports))
        return self


    def fetch(self):
        return list(self)


    def run(self):
        return iter(self)


    def __iter__(self):
        '''Returns an iterator over the result'''
        return self.api_client._fetchpages('leagues', 
                                    'leagues', League.from_dict, **self.params)


class StandingsQuery(ApiQuery):

    def __init__(self, api_client, league_id):
        super(StandingsQuery, self).__init__(api_client)
        self.league_id = league_id

    def round(self, x):
        self.params['round'] = x
        return self

    def fetch(self):
        return list(self)         

    def run(self):
        return iter(self)


    def __iter__(self):

        endpoint = "leagues/" +str(self.league_id)+"/standings"
        data = self.api_client._fetchresource(endpoint, **self.params)

        for group in data.get('groups', []):
            group_labels = group.get('labels', [])
            for standing in group.get('standings', []):
                yield Standing.from_dict(standing, group_labels)



class EventsQuery(ApiQuery):
    '''A query for one or many events. 

    '''

    def leagues(self, *league_ids):
        self.params['league'] = ",".join(map(str,league_ids)) 
        return self  


    def fromdate(self, d):
        '''Queries events from this date'''
        self.params['fromDate'] = d.strftime("%Y-%m-%d")
        return self

    
    def todate(self, d):
        '''Queries events to this date'''
        self.params['toDate'] = d.strftime("%Y-%m-%d")
        return self


    def today(self):
        '''Queries today's events'''
        today = datetime.date.today()
        self.params['toDate'] = self.params['fromDate'] = today.strftime('%Y-%m-%d')
        return self 


    def upcoming(self):
        '''Queries for all upcoming events'''
        self.params['status'] = "UPCOMING"
        return self

    def finished(self):
        '''Queries for all finished events'''
        self.params['status'] = "FINISHED"
        return self

    def sport(self, *sports):
        '''Queries events for one or many sports, by Sport ID'''
        self.params['sport'] = ",".join(map(str, sports))
        return self

    def teams(self, *teams):
        '''Queries events for one or many teams, by Team ID'''
        self.params['team'] = ",".join(map(str,teams))
        return self

    def round(self, *x):
        '''Queries for a specific round '''
        self.params['round'] = ",".join(map(str,x))
        return self 


    def fetch(self):
        return list(self)


    def run(self):
        return iter(self)


    def __iter__(self):
        '''Returns an iterator'''
        self.endpoint =  'events'
        return self.api_client._fetchpages('events', 
                            'events', Event.from_dict, **self.params)



