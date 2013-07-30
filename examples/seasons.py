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
        print "{} : {}, {} -- {}".format(league.sport.name.encode('utf-8'),league.name.encode('utf-8'), league.season.starts("%y-%m-%d"), league.season.ends("%y-%m-%d"))
    else:
        print "{} : {},".format(league.sport.name.encode('utf-8'), league.name.encode('utf-8'))








