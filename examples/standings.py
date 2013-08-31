#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Examples of getting a specific league and work with standings'''

import os
import everysport


APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(APIKEY)

allsvenskan = es.get_standings(57973)
nhl = es.get_standings(58878)


#Standings for complete league
print allsvenskan.league


#Standings by group types in NHL
for group_type in nhl.grouptypes: # e.g. 'conference'
    print group_type.upper()    
    for group_name in nhl.get_groupnames_by_type(group_type):         
        print nhl.get_group_by_name(group_name)


    











