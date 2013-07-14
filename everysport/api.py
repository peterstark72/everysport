#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A simple library that wraps the Everysport API. 

'''


import datetime
import logging


from events import EventsList as EventsList
from events import Event as Event
from standings import StandingsGroupsList as StandingsGroupsList
from results import get_results_for_leagues as get_results_for_leagues


import url_builder


class EverysportException(Exception):
    pass


class Api(object):
    '''Everysport API client'''


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


    def get_results(self, *league_ids):
        '''Return results for given leagues

        Arguments:
        league_id - from everysport.com
        '''
        return get_results_for_leagues(self, *league_ids)
        

    def get_event(self, event_id):
        '''Returns an Event for a given id  

        Arguments:
        event_id - from everysport.com
        
        '''

        url = url_builder.get_event_url(event_id, apikey=self.apikey)

        try:
            event = Event.from_resource(url)    
        except Exception as e:
            m = u"Could not load event {} : {}".format(event_id, e.message)
            logging.warning(m)
            raise EverysportException(m)

        return event
            
 



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


    def fetchall(self):   
        '''Returns a StandingsGroupsList of all standings groups'''
        
        url = url_builder.get_standings_url(self.league_id, **self.params)

        return StandingsGroupsList.from_resource(url)





class EventsQuery(ApiQuery):
    '''A query for one or many events. 

    '''

    def __init__(self, api_client, *league_ids):
        super(EventsQuery, self).__init__(api_client)
        self.league_ids = league_ids


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


    def fetchall(self):
        '''Returns a list of ALL events. This can be large, 500+ items for some leagues'''
        return list(self)


    def __iter__(self):
        '''Generator over events.'''

        done = False
        while not done:
            
            url = url_builder.get_events_url(*self.league_ids, **self.params)
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







