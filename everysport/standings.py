#!/usr/bin/env python
'''Domain objects for Everysport Leagues

'''

from collections import namedtuple
from collections import defaultdict



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



class Standings(namedtuple('Standings', 
                "team stats position_statuses groups")):
    __slots__ = ()
    @classmethod
    def from_dict(cls, data, group_labels):
        return cls(
                Team.from_dict(data.get('team', {})), 
                Stats.from_list(data.get('stats', [])), 
                PositionStatuses.from_list(data.get('positionStatuses', [])), 
                map( lambda x:x['name'], group_labels)
            )



class StandingsList(list):
    '''List of Standings''' 


    def get_teamposition_and_stats(self, team):
        for name, group in self.groups().items():
            for pos, standing in enumerate(group, 1):
                if team.id == standing.team.id:
                    return pos, standing
        return None



    def group_labels(self):
        '''Returns a Set of group labels for this league'''
        group_labels = ()
        for standing in self:
            for group_label in standing.groups:
                group_labels.append(group_label)

        return group_labels


    def groups(self):
        '''Returns standings by group name'''
        groups = defaultdict(list)
        for standing in self:
            if not standing.groups:
                groups['default'].append(standing)
            for group_label in standing.groups:
                groups[group_label].append(standing)
        return groups



    def get_group_by_name(self, name):
        '''Returns standings for the group whose name first matches the given name'''
        for group in self.groups():
            if group == name:
                return group


    def all_teams(self):
        '''Returns an iterator of all teams in this league'''
        return [standing.team for standing in self]








            







    