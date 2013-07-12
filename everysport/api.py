#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A simple library that wraps the Everysport API. 

'''


import datetime
import urllib
import logging

from data import Event, EventsList, StandingsGroupsList, LeagueResults


BASE_API_URL = "http://api.everysport.com/v1/{}"




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


    def events(self, *league_ids):
        '''Returns a Query object for events from one or many leagues

        Arguments:
        league_ids - from everysport.com

        '''
        return EventsQuery(self, *league_ids)


    def standings(self, league_id):
        '''Returns a Query object for standings

        Arguments:
        league_id - from everysport.com

        '''
        
        return StandingsQuery(self, league_id)



    def get_results(self, league_id):
        '''Returns results for each team in the league'''
        return LeagueResults(self, league_id)

        

    def get_event(self, event_id):
        '''Returns an Event for a given id  

        Arguments:
        event_id - from everysport.com
        
        '''
        
        params = {'apikey': self.apikey}

        url = UrlBuilder().event(event_id).with_params(params).build()

        return Event.from_resource(url)    
            
 

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


    def getall(self):   
        '''Returns a StandingsGroupsList of all standings groups'''
        
        url = UrlBuilder().standings(self.league_id).with_params(self.params).build()

        return StandingsGroupsList.from_resource(url)





class EventsQuery(ApiQuery):
    '''A query for one or many events. 

    '''

    def __init__(self, api_client, *league_ids):
        super(EventsQuery, self).__init__(api_client)
        self.params['league'] = ",".join(map(str, league_ids))


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


    def getall(self):
        '''Returns a list of ALL events. This can be large, 500+ items for some leagues'''

        events = []
        for event in self:
            events.append(event)
        return events    


    def __iter__(self):
        '''Generator over events.'''

        done = False
        while not done:
            
            url = UrlBuilder().events().with_params(self.params).build()
            try:
                result = EventsList.from_resource(url)
            except:
                raise StopIteration
            
            done = result.count == 0 
            if not done:
                for ev in result:
                    yield ev
                self.params['offset'] = result.offset + result.count
            done = result.count < result.limit







