#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport



EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


api = everysport.Api(EVERYSPORT_APIKEY)

allsvenskan = api.standings(everysport.ALLSVENSKAN)
nhl = api.standings(everysport.NHL)



for standings in nhl:
    print standings


for name, group in nhl.list().groups().items():
    print name, group
    

for standings in allsvenskan:
    print standings.team.name.encode('utf-8'), standings.stats.pts






