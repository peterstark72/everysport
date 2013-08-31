#!/usr/bin/env python
'''Example use of leagues query'''

import os

import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)

#Print all current swedish hockey leagues
for league in es.leagues.hockey().sweden():
    print league







