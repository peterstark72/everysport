#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Miscellenous examples'''

import os
import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)



# Get all arenas today
for e in es.events.today():
    print e.arena


# Find out when football season ends
for league in es.leagues.football():
    print league.name.encode('utf-8'), league.season.ends("%d/%m")








