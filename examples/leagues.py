#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

api = everysport.Api(EVERYSPORT_APIKEY)

hockey = api.leagues().sport(everysport.HOCKEY)

for league in hockey:
    print league








