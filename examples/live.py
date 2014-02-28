#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Example with Live events

'''
import os
import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)


for event in es.events.ongoing().today():
    print event