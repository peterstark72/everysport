#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''commons.py
Common Everysport classes and function.

'''

import datetime
from collections import namedtuple

class Date(datetime.datetime):
    '''Everysport Date object. Timezone is always CEST and it's created from the Everysport API Date format'''
    def __new__(cls, data):
        if data and len(data)>16:
            d = datetime.datetime.strptime(data[0:16],"%Y-%m-%dT%H:%M" )
            return datetime.datetime.__new__(cls, d.year, d.month, d.day, d.hour, d.minute)



class IdentityObject(namedtuple('IdentityObject', "id name")):
    '''A tuple with an ID and a name'''
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            data.get('name', None)
        )

    def __str__(self):
        return self.name.encode('utf-8')

    def __eq__(self, other):
        return self.id == other.id  


