#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''team.py

Everysport teams are defined with an ID. They always have a name, and may also have a short name and an abbreviation.


'''

from collections import namedtuple


class Team(namedtuple('Team', "id, name, short_name, abbreviation")):
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
            data.get('name', None),
            data.get('short_name', None),
            data.get('abbreviation', None)
        )

    def __repr__(self):
        return "Team({})".format(self.name.encode('utf-8'))


    def __eq__(self, other):
        return self.id == other.id



MFF = Team(9375,u"Malmö FF", "", "")
HIF = Team(9373,u"Helingsborgs IF", "", "")
LSD = Team(1175,u"Leksand", "", "")
CHI = Team(28075,u"Chicago Blackhawks", "", "")
        