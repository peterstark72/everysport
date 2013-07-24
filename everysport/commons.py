#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Everysport Domain Objects

See Everysport API documentation at:
https://github.com/menmo/everysport-api-documentation

'''

from collections import namedtuple
import datetime


class Date(datetime.datetime):
    '''A Date object for swedish time'''
    timezone = "CEST"
    @classmethod
    def from_str(cls, d):
        return cls.strptime(d[0:16],"%Y-%m-%dT%H:%M" )

    def daysuntil(self):
        '''Returns number of days from today'''
        pass



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


class Facts(namedtuple('Facts', "arena, spectators, referees, shots")):
    __slots__ = ()
    @classmethod
    def from_dict(cls, data):
        return cls(
            Arena.from_dict(data.get('arena', {})),
            data.get('spectators', None),
            data.get('referees', []), #list of names
            data.get('shots', None),
        )



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



class Standing(namedtuple('Standing', 
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

