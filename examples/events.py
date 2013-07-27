#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

api = everysport.Api(EVERYSPORT_APIKEY)

football_today = api.events().sport(everysport.FOOTBALL).today()

for event in football_today:
    print event






