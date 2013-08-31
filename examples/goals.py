#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Example use of game events: goals'''

import os

import everysport


APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)


games = es.events.leagues(57973).finished().allfields().fetch()


for goal in games.goals:
    print goal






