#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(EVERYSPORT_APIKEY)


for event in es.events.sport("Football").yesterday():
    print event






