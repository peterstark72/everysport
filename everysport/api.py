#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A wrapper for the Everysport API. 

'''

import urllib
import urllib2
import datetime
import logging
import hashlib
import json

from events import Event
from standings import Standings, StandingsList


BASE_API_URL = "http://api.everysport.com/v1/{}"


class EverysportException(Exception):
    '''Exception for the Everysport module'''
    pass


class Api(object):
    '''Everysport API client'''


    def __init__(self, apikey):     
        '''Create an API client

        Arguments:
        apikey - See instructions at 
                https://github.com/menmo/everysport-api-documentation

        '''
        self.key = apikey


    def standings(self, league_id):
        '''Returns a StandingsQuery

        Arguments:
        league_ids - from everysport.com

        '''

        return StandingsQuery(self.key, league_id)


    def events(self, *league_ids):
        '''Returns an EventsQuery for one or many leagues.

        Arguments:
        league_ids - from everysport.com

        '''
        return EventsQuery(self.key, *league_ids)

        

    def event(self, event_id):
        '''Returns an Event for a given id  

        Arguments:
        event_id - from everysport.com
        
        '''
        return EventQuery(self.key, event_id)
            
 

class ApiQuery(object):

    cache = {}

    def __init__(self, apikey):
        self.params = {}
        self.params['apikey'] = apikey
        self.endpoint = ""


    def _send_query(self):
        '''Sends the Query and returns the response''' 

        url = BASE_API_URL.format(self.endpoint) + "?" + urllib.urlencode(self.params)

        #Check if already in cache, else add it
        key = hashlib.md5(url).hexdigest()
        if key not in ApiQuery.cache:
            logging.info("Loading {}".format(url))
            try:
                response = urllib2.urlopen(url)
                ApiQuery.cache[key] = json.load(response)
            except Exception as e:
                raise EverysportException('Could not load {} with {} : \n{}'.format(url, self.params, e.message))

        return ApiQuery.cache[key]




class EventQuery(ApiQuery):
    '''Query for a specific Event'''

    def __init__(self, apikey, event_id):
        super(EventQuery, self).__init__(apikey)
        self.endpoint = 'events/'+str(event_id)

    def get(self):
        data = self._send_query()
        return Event.from_dict(data.get('event', {}))


class StandingsQuery(ApiQuery):

    def __init__(self, apikey, league_id):
        super(StandingsQuery, self).__init__(apikey)
        self.endpoint = 'leagues/'+str(league_id)+"/standings"

    def round(self, x):
        self.params['round'] = x
        return self

    def list(self):
        standings_list = StandingsList()
        for s in self:
            standings_list.append(s)
        return standings_list

    def __iter__(self):

        data = self._send_query()        
        
        for group in data.get('groups', []):
            group_labels = group.get('labels', [])
            for standing in group.get('standings', []):
                yield Standings.from_dict(standing, group_labels)



class EventsQuery(ApiQuery):
    '''A query for one or many events. 

    '''

    def __init__(self, apikey, *league_ids):
        super(EventsQuery, self).__init__(apikey)
        self.endpoint = 'events'
        self.params['league'] = ",".join(map(str,league_ids))    


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


    def __iter__(self):
        '''Returns an iterator'''

        done = False
        while not done:
            try:
                data = self._send_query()                    
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
                self.params['offset'] = offset + count
            done = count < limit 







