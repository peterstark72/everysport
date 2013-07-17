#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import everysport
from everysport.encoders import json_dumps


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


api = everysport.Api(EVERYSPORT_APIKEY)

results = api.get_results(everysport.ALLSVENSKAN)


for teamresult in results:
    print teamresult.team.name.encode('utf-8')
    print teamresult.stats.pts
    print teamresult.results[0].events[0]


print json_dumps(results)

