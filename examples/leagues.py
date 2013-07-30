#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Example ise of everysport.leagues query'''

import os
import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)

for league in es.leagues.hockey():
    print league








