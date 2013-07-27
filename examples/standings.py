#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

api = everysport.Api(EVERYSPORT_APIKEY)

nhl = api.league(everysport.NHL).standings()


print nhl #Complete league, all teams


for g in nhl.groups(): 
    print g #The groups


for g in nhl.groups('conference'): 
    print g #Conferences


print nhl.group("Western Conference")


