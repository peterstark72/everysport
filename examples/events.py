#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport

es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'])

for e in es.events.football().today():
    print e








