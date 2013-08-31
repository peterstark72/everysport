#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Example use of game events'''

import os

import everysport


APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)


#Fetch list of all finished events in Allsvenskan 
games = es.get_events_query().leagues(57973).finished().allfields().fetch()


#Print all events in CSV format
import csv

writer = csv.writer(open("allsvenska_goals-20130830.csv", "w"))

writer.writerow(["minute", "team", "player"])

for goal in games.goals:
    writer.writerow(
        [ goal['minute'], goal['team']['name'].encode('utf-8'), goal['player']['name'].encode('utf-8')]
        )







