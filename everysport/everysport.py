#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''everysport.py


'''

import datetime
import urllib
import urllib2
import json
import functools
import logging



class EverysportException(Exception):
    '''Exception for the Everysport module'''
    pass


class Everysport(object):
    '''A Python wrapper for the Everysport API

    Example usage: 

    #Create Everysport object 
    es = everysport.Everysport(APIKEY)
    
    #Leagues
    nhl = es.get_league(everysport.NHL)


    '''

    def __init__(self, apikey):
        '''Initialize an instance of Everysport with your APIKEY'''
        self.apikey = apikey  


    def get_league(self, league_id):
        '''Returns a League object

        Arguments:
        league_id - the league ID from everysport.com

        '''
        endpoint = "leagues/" + str(league_id)
        response = _get_resource(endpoint, apikey=self.apikey) 
        return response.get('league', {})

    @property
    def leagues(self):
        '''Returns a LeaguesQuery'''
        return LeaguesQuery(self.apikey)

    @property
    def events(self):
        '''Returns an EventsQuery'''
        return EventsQuery(self.apikey)


    def get_event(self, event_id):
        '''Returns an Event object

        Arguments:
        event_id - the event ID from everysport.com.

        '''
        endpoint = "events/" + str(event_id)
        response = _get_resource(endpoint, apikey=self.apikey) 
        return response.get('event', {})


    def get_events_for_league(self, league_id):
        '''Returns a EventsQuery'''
        return EventsQuery(self.apikey).leagues(league_id)


    def get_standings(self, league_id, r="", t="total"):
        '''Gets standings for a league.

        Arguments:
        league_id - the League ID
        r - The round number, e.g. 1,2,3,...
        t - One of "total", "home", "away". 

        '''
        endpoint = "leagues/" +str(league_id)+"/standings"
        response = _get_resource(endpoint, 
                                apikey=self.apikey, 
                                round=r, 
                                type=t)
        return StandingsGroupsList(response.get('groups', []))


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
    'volleyball': 11
}

class SportQueryAccumulator:
    '''This is used by ApiQuery class to generate the sport query functions such as football() and hockey().'''
    def __init__(self, query_obj, sport_id):
        self.query_obj = query_obj
        self.sport_id = sport_id

    def __repr__(self):
        return self.sport_id

    def __call__(self):
        return self.query_obj.sport(self.sport_id)


class ApiQuery:
    '''Abstract object for Queries against the API'''

    def __init__(self, apikey):
        self.params = {}
        self.params['apikey'] = apikey

        for name, value in SPORT_ID_MAP.items():
            setattr(self, name, SportQueryAccumulator(self, value))

    
    def sport(self, *sports):
        '''Queries events for one or many sports, by Sport ID'''
        self.params['sport'] = ",".join(map(str, sports))
        return self




class LeaguesQuery(ApiQuery):
    '''Query for leagues'''

    def sweden(self):
        '''Returns only swedish leagues'''
        self.params['country'] = "se"
        return self        

    def __iter__(self):
        '''Returns an iterator over the result'''
        return _fetch_pages('leagues', 'leagues', **self.params)

    def fetch(self):
        return list(self)


class StandingsGroupsList(list):

    @property
    def grouptypes(self):
        '''The different group types for this league. Returns a set.'''
        return {g['type'] for s in self for g in s.get('labels', [])}

    @property
    def groupnames(self):
        '''The different group name for this league. Returns a set.'''
        return {g['name'] for s in self for g in s.get('labels', [])}

    @property
    def teams(self):
        '''List of all teams. '''
        return [s['team'] for group in self for s in group.get('standings', [])]

    @property
    def league(self):
        '''Standings for the complete league, all groups'''
        all_standings = []
        for group in self:
            all_standings.extend(group.get('standings', []))
        return all_standings

    def get_groupnames_by_type(self, group_type):
        '''Group names for the given type'''
        return {label['name'] for group in self for label in group['labels'] if group_type==label['type']} 


    def get_groups_by_type(self, group_type):
        '''Groups of the given type'''
        return [group for group in self if group_type in [label['type'] for label in group['labels']]]


    def get_group_by_name(self, group_name):
        '''Gets the group with the given name'''
        groups = []
        for group in self:
            names = [label['name'] for label in group['labels']]
            if group_name in names:
                return group


    def get_stats_for_team(self, team_id):
        for group in self:
            for standing in group.get('standings', []):
                team = standing.get('team', {})
                if team_id == team.get('id', None):
                    return { s['name'] : s['value'] for s in standing.get('stats', [])}



class EventsList(list):
    '''A list of Event objects. This is what you get back when you fetch an EventQuery'''

    @property
    def gameevents(self):
        '''Returns list of all gameevents from the events'''
        all_gameevents = []
        for result in self:
            all_gameevents.extend(result.get('gameEvents', []))
        return all_gameevents

    @property      
    def goals(self):
        '''Returns list of all goals from the events'''
        return [ev for ev in self.gameevents if ev['type'] == "GOAL"]
    
    @property
    def warnings(self):
        '''Returns list of all warnings from the events'''
        return [ev for ev in self.gameevents if ev['type'] == "WARNING"]


class EventsQuery(ApiQuery):
    '''A query for one or many events. '''

    def leagues(self, *league_ids):
        '''Queries for one or many leagues'''
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

    def teams(self, *team_ids):
        '''Queries events for one or many teams, by Team ID'''
        self.params['team'] = ",".join(map(str,team_ids))
        return self

    def round(self, *x):
        '''Queries for one or many rounds'''
        self.params['round'] = ",".join(map(str,x))
        return self 


    def allfields(self):
        '''Includes all fields in response, e.g. game events'''
        self.params['fields'] = "all"
        return self


    def __iter__(self):
        '''Returns an iterator over the events'''
        return _fetch_pages('events', 'events', **self.params)

    def fetch(self):
        '''Fetches the entire list of events into an EventsList object'''
        return EventsList(self)



def cache(fn):

    _cache = {}

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in _cache:
            ret = _cache[key]
        else:
            ret = _cache[key] = fn(*args, **kwargs)

        return ret

    return wrapper


@cache
def _get_resource(endpoint, **params):
    '''This is used to fetch the resource at a given API endpoint. It's used by the Everysport object itself''' 

    BASE_API_URL = "http://api.everysport.com/v1/{}"

    url = BASE_API_URL.format(endpoint) + "?" + urllib.urlencode(params)    

    try:
        response = urllib2.urlopen(url)
        logging.debug("Getting {}".format(url))
        return json.load(response)

    except Exception as e:                
        raise EverysportException('Could not load {} with {} : \n{}'.format(url, params, e.message))



def _fetch_pages(endpoint, entity, **params):
    '''This is used to fetch several pages of a resource, such as a long list of events. It's used by the Everysport object itself.

        The function is a Generator and yields one item at at time. 

    ''' 

    done = False
    while not done:
        try:
            data = _get_resource(endpoint, **params)    

            page = data.get(entity, [])           

            offset = data['metadata']['offset']
            limit = data['metadata']['limit']
            count = data['metadata']['count']
        except:
            raise StopIteration
        
        done = count == 0 
        if not done:
            for d in page:
                yield d
            params['offset'] = offset + count
        done = count < limit 





