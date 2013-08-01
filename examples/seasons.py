#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Example with League seasons

'''

import os
import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)


for league in es.leagues:
    if league.season:
        print league.season








