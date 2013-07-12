#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

The Everysport domain data objects

'''

from collections import namedtuple
import datetime
import urllib2
import logging
import hashlib
import json


class EverysportException(Exception):
    pass


cache = {}

def getresource(url):
    '''Returns the resource at the url. Raises EverysportException'''

    #Check if already in cache, else add it
    key = hashlib.md5(url).hexdigest()
    if key not in cache:
        logging.info("Loading {}".format(url))
        try:
            response = urllib2.urlopen(url)
            cache[key] = json.load(response)
        except Exception as e:
            raise EverysportException("Could not load {} because {}".format(url,e.message))

    return cache[key]



class Team(namedtuple('Team', "id, name, short_name, abbreviation")):
    __slots__ = () #prevent creation of instance dict
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            data.get('name', None),
            data.get('short_name', None),
            data.get('abbreviation', None)
        )



class Sport(namedtuple('Sport', "id, name")):
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            data.get('name', None)
        )


class Arena(namedtuple('Arena', "id, name")):
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            data.get('name', None)
        )


class Label(namedtuple('Label', "name, type")):
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('name', None),
            data.get('type', None)
        )


class Credit(namedtuple('Credit', "message, link, logoUrl")):
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('message', None),
            data.get('link', None),
            data.get('logoUrl', None)
        )


class League(namedtuple('League', "id, name, sport, team_class")):
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            data.get('name', None),
            Sport.from_dict(data.get('sport', {})),
            data.get('team_class', None),
        )



class Facts(namedtuple('Facts', "arena,spectators,referees,shots")):
    __slots__ = ()
    @classmethod
    def from_dict(cls, data):
        return cls(
            Arena.from_dict(data.get('arena', {})),
            data.get('spectators', None),
            data.get('referees', []), #list of names
            data.get('shots', None),
        )



class Event(namedtuple('Event', "id, start_date, time_zone, round, status, home_team, visiting_team, home_team_score, visiting_team_score, finished_time_status, league,facts")):
    __slots__ = ()

    STATUS_FINISHED = "FINISHED"

    @classmethod    
    def from_dict(cls, data):
        try:
            d = data['startDate'][0:16]
            start_date = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M")
        except:
            start_date = None

        return cls(
                data.get('id', None),
                start_date,
                "CEST",
                data.get('round',None),
                data.get('status',None),
                Team.from_dict(data.get('homeTeam',{})),
                Team.from_dict(data.get('visitingTeam',{})),
                data.get('homeTeamScore',None),
                data.get('visitingTeamScore',None),
                data.get('finishedTimeStatus',None),
                League.from_dict(data.get('league',{})),
                Facts.from_dict(data.get('facts', {}))
            )


    @classmethod    
    def from_resource(cls, url):

        data = getresource(url)     

        return cls.from_dict(data.get('event', {}))


    def is_finished(self):
        return self.status == Event.STATUS_FINISHED



class Stats(object):    
    @classmethod    
    def from_list(cls, data):
        '''We get this as list of name/value pairs from the API'''
        
        obj = cls.__new__(cls)
        
        for stat in data:
            setattr(obj,stat['name'],stat['value'])
        
        return obj



class PositionStatus(namedtuple('PositionStatus', "name, type")):
    __slots__ = ()
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('name', None),
            data.get('type', None))


class PositionStatuses(list):
    @classmethod    
    def from_list(cls, data):
        '''We get this as list of name/value pairs from the API'''
        
        obj = cls.__new__(cls)
        
        for status in data:
            obj.append(PositionStatus.from_dict(status))
        
        return obj



class Standings(namedtuple('Standings', "team, stats, position_statuses")):
    __slots__ = ()
    @classmethod    
    def from_dict(cls, data):
        return cls(
            Team.from_dict(data.get('team', {})),
            Stats.from_list(data.get('stats',[])),
            PositionStatuses.from_list(data.get('positionStatuses',  []))
            )



class StandingsGroup(namedtuple('StandingsGroup', "labels, standings")):
    __slots__ = ()
    @classmethod    
    def from_dict(cls, data):

        labels = []
        for lbl in data.get('labels', []):
            labels.append(Label.from_dict(lbl))


        standings = []
        for sta in data.get('standings', []):
            standings.append(Standings.from_dict(sta))
            
        return cls(labels, standings)



'''

Resources 

'''
class EventsList(list):
    @classmethod
    def from_resource(cls, url):

        data = getresource(url)

        obj = cls.__new__(cls)

        for ev in data.get('events',[]):
            obj.append(Event.from_dict(ev))

        obj.credit = Credit.from_dict(data.get('credit', {}))
        
        obj.offset = data['metadata']['offset']
        obj.limit = data['metadata']['limit']
        obj.count = data['metadata']['count']

        return obj      




class StandingsGroupsList(list):
    @classmethod
    def from_resource(cls, url):

        response = getresource(url)

        obj = cls.__new__(cls)             

        for group in response.get('groups', []):
            obj.append(StandingsGroup.from_dict(group))

        return obj

    def get_teamposition(self, team):
        '''Returns the position for a given team'''

        for group in self:
            for pos, teamstats in enumerate(group.standings):
                if teamstats.team.id == team.id:
                    return pos + 1
        return None 


    def get_teamstats(self, team):
        '''Returns Stats for given team'''

        for group in self:
            for teamstats in group.standings:
                if teamstats.team.id == team.id:
                    return teamstats
        return None                    


    def get_teams(self):
        '''Returns the list of teams in the standings'''
        teams = []
        for group in self:
            for teamstats in group.standings:
                teams.append(teamstats.team)
        return teams
    


class Result(namedtuple("Result", "round, ga, gf, diff, pos, pos_change, against")):
    __slots__ = ()
    def _asjson(self):
        return {
            'against': self.against._asdict(),
            'round' : self.round,
            'ga' : self.ga,
            'gf' : self.gf,
            'diff' : self.diff,
            'pos' : self.pos,
            'posChange' : self.pos_change
        }



class Results(dict):
    '''List of Results '''  

    def __init__(self, api_client, league_id):

        for event in api_client.events(league_id).finished():

            #Get standings for this round
            standings = api_client.standings(event.league.id).round(event.round).getall()

            if event.home_team.id not in self:
                self[event.home_team.id] = []
         
            self[event.home_team.id].append(Result(
                event.round,
                event.visiting_team_score,
                event.home_team_score,
                event.home_team_score - event.visiting_team_score,
                standings.get_teamposition(event.home_team),
                0,
                event.visiting_team))


            #Add visiting team stats

            if event.visiting_team.id not in self:
                self[event.visiting_team.id] = []

            self[event.visiting_team.id].append(Result(
                event.round,
                event.home_team_score,
                event.visiting_team_score,
                event.visiting_team_score - event.home_team_score,
                standings.get_teamposition(event.visiting_team),
                0,
                event.home_team)) 



    def sorted(self):
        for team in self:
            self[team] = sorted(self[team], key=lambda x:x.round)
        return self




class LeagueResults(list):

    def __init__(self, api_client, league_id):

        standings = api_client.standings(league_id).getall()

        results = Results(api_client, league_id)

        for group in standings:
            for teamstats in group.standings:
                self.append({
                    'team' : teamstats.team,
                    'results' : results[teamstats.team.id],
                    'stats' : teamstats.stats
                    })


    def _asjson(self):   
        obj = []

        for result in self:
            result_obj = {}
            result_obj['team'] = result['team']._asdict()
            result_obj['results'] = map(Result._asjson, result['results'])
            result_obj['stats'] = result['stats'].__dict__
            obj.append(result_obj)

        return json.dumps(obj)



