#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''standings.py


'''
from collections import namedtuple
from collections import defaultdict

from team import Team

STATS = ('gp', 'w', 'd', 'l', 'gf', 'ga', 'diff', 'pts')

class Stats(namedtuple("Stats", STATS)):
    __slots__ = ()
    @classmethod
    def from_dict(cls, data):
        stats_data = []
        for s in STATS:
            stats_data.append(data.get(s, None))
        return cls._make(stats_data)


class TeamStanding(namedtuple('TeamStanding', "team stats status groups")):
    '''A team's Standing consists of the  Team, it's Stats, status and the groups it plays in.'''
    __slots__ = ()
    @classmethod
    def from_dict(cls, data, group_labels):
        return cls(
            Team.from_dict(data.get('team', {})), 
            Stats.from_dict({ stat['name'] : stat['value'] for stat in data.get('stats', [])}),
            data.get('positionStatuses', []), 
            group_labels)


    def __repr__(self):
        return "TeamStanding({})".format(",".join(map(repr, [self.team, self.stats])))


class Standings(list):
    '''List of Everysport Standings for a league'''

    def __init__(self, groups):
        for group in groups:
            group_labels = group.get('labels', [])
            for standing in group.get('standings', []):
                self.append(TeamStanding.from_dict(standing, group_labels))

    @classmethod
    def find(cls, api_client, league_id, round_="", type_="total"):
        endpoint = "leagues/" +str(league_id)+"/standings"
        data = api_client._fetchresource(endpoint, round=round_, type=type_)
        return cls(data.get('groups', []))


    def __repr__(self):
        return "Standings({})".format(",".join(map(repr, self)))


    def league(self):
        '''Returns list of standings for all teams in the league'''
        return self


    def grouptypes(self):
        '''Returns set of available group types. This may be empty if there are no groups. 
        '''
        return {g['type'] for s in self for g in s.groups}


    def groups(self, group_type=None):
        '''Returns defaultdict of groups in the league. If there are different types of groups in the league, e.g. as in NHL, use 'group_type' to filter just one type of group. 

            In NHL, the group types are 'conference' and 'division'. 

            Args:
            group_type - select only groups of this type            


        '''
        groups = defaultdict(list)
        for s in self:
            for g in s.groups:
                name = g['name'].strip() #Remove extra whitespace
                if not group_type or group_type==g['type']:
                    groups[name].append(s)
        return groups


    def group(self, name):
        return [s for s in self if name in [g['name'] for g in s.groups]]


    def getteamposition(self, team, group_name=None):

        if not group_name:
            position_group = self
        else:
            position_group = self.group(group_name)

        for pos, standing in enumerate(position_group,1):
            if standing.team == team:
                return pos


    def getstats(self, team):
        for s in self:
            if s.team == team:
                return s.stats









