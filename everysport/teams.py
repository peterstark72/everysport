#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

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

