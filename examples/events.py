#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


api = everysport.Api(EVERYSPORT_APIKEY)


for event in api.events(everysport.ALLSVENSKAN):
    print event


for event in api.events(everysport.ALLSVENSKAN).today():
    print event


swe_elite_football = api.events(everysport.ALLSVENSKAN, everysport.SUPERETTAN)
for event in swe_elite_football:
    print event



