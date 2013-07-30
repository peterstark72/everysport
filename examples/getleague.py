#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Examples of getting a specific league and work with standings'''

import os
import everysport


APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(APIKEY)

allsvenskan = es.getleague_by_name("Allsvenskan", "football")
nhl = es.getleague_by_name("NHL", "hockey")


#Standings for complete League
print allsvenskan.totals
print allsvenskan.round(6).totals


#Standings by group types in NHL
for group_type in nhl.standings.grouptypes(): # e.g. 'conference'
    
    for group in nhl.standings.groups(group_type): 
        print group.upper()
    
        for standings in nhl.standings.group(group):
            print standings 











