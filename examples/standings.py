#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


api = everysport.Api(EVERYSPORT_APIKEY)

standings = api.standings(everysport.ALLSVENSKAN).total().fetchall()        
allsvenskan = standings.group()        

for teamstats in allsvenskan.standings:
    print teamstats


