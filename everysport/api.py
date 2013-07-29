#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''api.py


'''

import urllib
import urllib2
import datetime
import logging
import json


from league import League
from event import Event
import simplecache as simplecache


BASE_API_URL = "http://api.everysport.com/v1/{}?apikey={}"




class EverysportException(Exception):
    '''Exception for the Everysport module'''
    pass


class Everysport(object):
    '''A Python wrapper for the Everysport API

    Example usage: 

    #Create Everysport object 
    es = everysport.Everysport(APIKEY)
    
    #NHL
    nhl = es.getleague(everysport.NHL)
    

    hockey_leagues = es.leagues.sport("Hockey")
    football_leagues = es.leagues.sport("Football")

    '''

    _cache = {}

    def __init__(self, apikey):
        self.apikey = apikey  

    def getleague(self, league_id):
        '''Returns a League given League ID '''
        return League.find(self, league_id) 

    def getleague_by_name(self, name, sport):
        '''Looks up a league given name and sport

        This only works for current leagues, on everysport.com today. To get older leagues, you need the ID and use getleague() method. 

        ''' 
        spork_key = sport.lower()
        for league in self.leagues.sport(SPORT_ID_MAP.get(spork_key, None)):
            if league.name == name:
                return league  


    def getevent(self, event_id):
        '''Returns an Event object'''
        return Event.find(self, event_id)


    @property
    def leagues(self):
        '''Returns LeaguesQuery'''
        return LeaguesQuery(self)
    
    @property 
    def events(self):
        '''Returns EventsQuery'''
        return EventsQuery(self)


    def _fetchresource(self, endpoint, **params):
        '''Sends the Query and returns the response''' 

        if params:
            url = BASE_API_URL.format(endpoint, self.apikey) + "&" + urllib.urlencode(params)
        else:
            url = BASE_API_URL.format(endpoint, self.apikey)


        #Check if already in cache, else add it
        data = simplecache.geturl(url)
        if data is not None:
            return data
        else:            
            try:
                response = urllib2.urlopen(url)
                data = json.load(response)
                logging.debug("Fetched {} from {}".format(len(data), url))
                simplecache.addurl(url, data)
                return data
            except Exception as e:                
                raise EverysportException('Could not load {} with {} : \n{}'.format(url, params, e.message))



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




SPORT_ID_MAP = {
'american_football': 18,
'badminton': 9,
'bandy': 3,
'baseball': 20,
'basket': 5,
'table_tennis': 8,
'bowling': 1,
'wrestling': 16,
'football': 10,
'handball': 7,
'floorball': 4,
'hockey': 2,
'rugby': 17,
'softball': 68,
'speedway': 15,
'squash': 22,
'tennis': 19,
'volleyball': 11}


class SportQueryAccumulator:
    def __init__(self, query_obj, sport_id):
        self.query_obj = query_obj
        self.sport_id = sport_id

    def __repr__(self):
        return self.sport_id

    def __call__(self):
        return self.query_obj.sport(self.sport_id)



class ApiQuery:
    '''Abstract object for Queries against the API'''

    def __init__(self, api_client):
        self.api_client  = api_client
        self.params = {}

        for name, value in SPORT_ID_MAP.items():
            setattr(self, name, SportQueryAccumulator(self, value))

    
    def sport(self, *sports):
        '''Queries events for one or many sports, by Sport ID'''
        self.params['sport'] = ",".join(map(str, sports))
        return self


    def fetch(self):
        return list(self)


    def run(self):
        return iter(self)        


class LeaguesQuery(ApiQuery):
    '''Query for leagues'''


    def __iter__(self):
        '''Returns an iterator over the result'''
        return self.api_client._fetchpages('leagues', 
                                    'leagues', League.from_dict, **self.params)



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


    def yesterday(self):
        '''Queries events from yesterday'''
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.params['toDate'] = self.params['fromDate'] = yesterday.strftime('%Y-%m-%d')
        return self         


    def upcoming(self):
        '''Queries for all upcoming events'''
        self.params['status'] = "UPCOMING"
        return self

    def finished(self):
        '''Queries for all finished events'''
        self.params['status'] = "FINISHED"
        return self

    def teams(self, *teams):
        '''Queries events for one or many teams, by Team ID'''
        self.params['team'] = ",".join(map(str,teams))
        return self

    def round(self, *x):
        '''Queries for a specific round '''
        self.params['round'] = ",".join(map(str,x))
        return self 


    def __iter__(self):
        '''Returns an iterator'''
        self.endpoint =  'events'
        return self.api_client._fetchpages('events', 
                            'events', Event.from_dict, **self.params)



