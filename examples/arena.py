#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Example with Arena for events

'''
import os
import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)

for event in es.events.today():
    if event.arena:
        print "{} : {}-{} @ {}".format(event.league.sport.name, event.hometeam.name.encode('utf-8'), event.visitingteam.name.encode('utf-8'), event.arena)
    else:
        print "{} : {}-{}".format(event.league.sport.name, event.hometeam.name.encode('utf-8'), event.visitingteam.name.encode('utf-8'))







