#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import everysport

import itertools


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


api = everysport.Api(EVERYSPORT_APIKEY)

results = api.get_results(everysport.ALLSVENSKAN)

for result in itertools.ifilter(lambda x:x.home, results):
    print u"{} - {}  {}-{}".format(result.team.name, result.against.name, result.gf, result.ga).encode('utf-8')


