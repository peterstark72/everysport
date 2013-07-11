#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A simple library that wraps the Everysport API. 

'''


import datetime
import urllib
import urllib2
import json
import logging
import hashlib

from data import Event, Events, Standings


BASE_API_URL = "http://api.everysport.com/v1/{}"


class EverysportException(Exception):
    pass


class Api(object):
    '''Everysport API client'''

    cache = {}

    def __init__(self, apikey):     
        '''Create an API client

        Arguments:
        apikey - See instructions at 
                https://github.com/menmo/everysport-api-documentation

        '''
        self.apikey = apikey


    def events(self):
        '''Returns a Query object for events'''
        return EventsQuery(self)

    def standings(self, league_id):
        '''Returns a Query object for standings'''
        return StandingsQuery(self, league_id)


    def teams(self, league_id):
        team_list = []
        for group in StandingsQuery(self, league_id):
            for teamstats in group.standings:
                team_list.append(teamstats.team)

        logging.debug("Teams list {}".format(team_list))
        return team_list        
        

    def get_event(self, event_id):
        '''Returns an Event for a given id  

        event_id - from everysport.com
        '''
        
        params = {'apikey': self.apikey}
        url = UrlBuilder().event(event_id).with_params(params).build()

        try:
            response = self.getresource(url)
        except:
            raise EverysportException('Could not load {}'.format(url))

        return Event.from_dict(response.get('event',None))    



    def getresource(self, url):
        '''Returns resource as Python object, deserielized from JSON 

        Arguments:
        url -- The API endpoint
        '''

        #Check if already in cache, else add it
        key = hashlib.md5(url).hexdigest()
        if key not in self.cache:
            logging.info("Requesting {}".format(url))
            response = urllib2.urlopen(url)
            self.cache[key] = json.load(response)

        return self.cache[key]             
 

class UrlBuilder(object):
    '''Builder for URLs for various endpoints'''
    def __init__(self):
        self.url = ""

    def standings(self, league_id):
        '''Builds URL for standings resource

        Arguments:
        league_id - from everysport.com

        '''
        endpoint = 'leagues/' + str(league_id) + '/standings'
        self.url = BASE_API_URL.format(endpoint)
        return self

    def events(self):
        '''Builds URL for standings resource'''
        endpoint = 'events'
        self.url = BASE_API_URL.format(endpoint)
        return self

    def event(self, event_id):
        '''Builds URL for event resource

        Arguments:
        event_id -- from everysport.com

        '''
        endpoint = 'events/' + str(event_id) 
        self.url = BASE_API_URL.format(endpoint)
        return self

    def with_params(self, params):
        '''Adds parameters to the URL

        Arguments:
        params - a dictionary with parameters to add to the URL

        '''
        encoded_params = urllib.urlencode(params)
        self.url += "?" + encoded_params 
        return self 

    def build(self):
        '''Returns the URL that has been built'''
        return self.url



class ApiQuery(object):
    '''Base class for all queries. '''
    def __init__(self, api_client):
        '''Initialized with the API and empty query '''
        self.api_client = api_client
        self.params = {}
        self.params['apikey'] = api_client.apikey


class StandingsQuery(ApiQuery):
    '''A Query for a league's standings (tables). In most leagues, just one. But e.g. NHL have many groups.

        Returns a list of StandingGroups. 
    '''    

    def __init__(self, api_client, league_id):
        super(StandingsQuery, self).__init__(api_client)
        self.league_id = league_id

    def total(self):
        '''Queries for Total standings '''
        self.params['type'] = 'total'
        return self

    def home(self):
        '''Queries for Home standings '''
        self.params['type'] = 'home'
        return self     

    def away(self):
        '''Queries for Away standings '''
        self.params['type'] = 'away'
        return self     

    def round(self, x):
        '''Queries for a specific round '''
        self.params['round'] = x
        return self 


    def __iter__(self):
        '''Returns an iterator (Standings) over all StandingGroups.'''
        
        url = UrlBuilder().standings(self.league_id).with_params(self.params).build()

        try: 
            response = self.api_client.getresource(url)
            result = Standings.from_dict(response)
        except:
            raise EverysportException("Could not load {}".format(url))

        return iter(result)




class EventsQuery(ApiQuery):
    '''A query for one or many events. 

    '''

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

    def leagues(self, *leagues):
        '''Queries for one or many leagues'''
        self.params['league'] = ",".join(map(str, leagues))
        return self     


    def __iter__(self):
        '''Generator that loads all events from the API.'''

        done = False
        while not done:
            
            url = UrlBuilder().events().with_params(self.params).build()
            try:
                response = self.api_client.getresource(url)
                result = Events.from_dict(response)
            except:
                raise StopIteration
            
            done = result.count == 0 
            if not done:
                for ev in result:
                    yield ev
                self.params['offset'] = result.offset + result.count
            done = result.count < result.limit







