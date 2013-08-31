#!/usr/bin/env python
'''Example use of leagues query'''

import os

import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']
es = everysport.Everysport(APIKEY)

#Get leagues query
q = es.get_leagues_query()

#Print all current swedish hockey leagues
for league in q.hockey().sweden():
    print league



#Print all current swedish football leagues
for league in q.football().sweden():
    print league






