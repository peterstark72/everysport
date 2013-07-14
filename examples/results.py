#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import everysport



EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


api = everysport.Api(EVERYSPORT_APIKEY)

results = api.get_results(everysport.ALLSVENSKAN)


for result in results:
    print result


