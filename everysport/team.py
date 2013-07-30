#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''team.py

Everysport teams are defined with an ID. They always have a name, and may also have a short name and an abbreviation.


'''

from collections import namedtuple
from commons import SportName

class Team(namedtuple('Team', "id name")):
    '''Team object

    Properties:
    id - Everysport Team ID
    name - e.g. "Malmö FF"
    short_name - e.g. "Malmö"
    abbreviation - e.g. "MFF"

    '''
    __slots__ = () 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id', None),
            SportName(
                data.get('name', None),
                data.get('short_name', None),
                data.get('abbreviation', None)
                )
        )

    def __repr__(self):
        return "Team({})".format(self.name)


    def __eq__(self, other):
        return self.id == other.id



if __name__ == '__main__':
    MFF = Team(9375,SportName(u"Malmö FF", None, None))
    HIF = Team(9373,SportName(u"Helingsborgs IF", None, None))
    LSD = Team(1175,SportName(u"Leksand", None, None))
    CHI = Team(28075,SportName(u"Chicago Blackhawks", None, None))


    print MFF



        