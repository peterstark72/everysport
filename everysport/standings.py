#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

standings.py


'''

from collections import namedtuple


from teams import Team as Team
from resource import getresource as getresource


class Label(namedtuple('Label', "name, type")):
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('name', None),
            data.get('type', None)
        )




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





class StandingsGroupsList(list):
    @classmethod
    def from_resource(cls, url):

        response = getresource(url)

        obj = cls.__new__(cls)             

        for group in response.get('groups', []):
            obj.append(StandingsGroup.from_dict(group))

        return obj


    def group(self,x=0):
        '''Returns the given group or None'''
        if len(self)>x:
            return self[x]
        else:
            return None

    def get_teamposition(self, team_id):
        '''Returns the position for a given team ID'''

        for group in self:
            for pos, teamstats in enumerate(group.standings,1):
                if teamstats.team.id == team_id:
                    return pos
        return None 


    def get_teamstats(self, team_id):
        '''Returns Stats for given team ID'''

        for group in self:
            for teamstats in group.standings:
                if teamstats.team.id == team_id:
                    return teamstats.stats
        return None                    


    def get_teams(self):
        '''Returns the list of teams in the standings'''
        teams = []
        for group in self:
            for teamstats in group.standings:
                teams.append(teamstats.team)
        return teams
    





