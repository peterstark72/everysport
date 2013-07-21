#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


api = everysport.Api(EVERYSPORT_APIKEY)


for event in api.events(everysport.ALLSVENSKAN).upcoming():
    print event


print api.event(2129802).get()





