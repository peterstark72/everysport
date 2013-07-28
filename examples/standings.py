#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(EVERYSPORT_APIKEY)

nhl_standings = es.getleague(everysport.NHL).standings


print nhl_standings #Complete league, all teams


for g in nhl_standings.groups(): 
    print g #The groups


for g in nhl_standings.groups('conference'): 
    print g #Conferences


print nhl_standings.group("Western Conference")


