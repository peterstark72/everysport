#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(EVERYSPORT_APIKEY)

hockey = es.leagues.sport("Hockey")

for league in hockey:
    print league








