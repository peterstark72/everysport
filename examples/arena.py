#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Example with Arena for events

'''
import os
import everysport

APIKEY = os.environ['EVERYSPORT_APIKEY']

es = everysport.Everysport(APIKEY)

for event in es.get_events_query().today():
    facts = event.get('facts', None)
    if facts:
        print facts.get('arena', {})







