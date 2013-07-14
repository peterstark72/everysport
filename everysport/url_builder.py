#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

import urllib
import logging

BASE_API_URL = "http://api.everysport.com/v1/{}"


def get_standings_url(league_id, **params):
    '''Builds URL for standings resource

    Arguments:
    league_id - from everysport.com

    '''
    url = BASE_API_URL.format('leagues/' + str(league_id) + '/standings')
    if len(params) > 0:
        return url + "?" + urllib.urlencode(params)
    return url


def get_events_url(*league_ids, **params):
    args = params
    url = BASE_API_URL.format('events')
    args['league'] = ",".join(map(str,league_ids))    
    return url + "?" + urllib.urlencode(args)    


def get_event_url(event_id, **params):
    url = BASE_API_URL.format('events/' + str(event_id)) + "?" + urllib.urlencode(params)
    logging.debug("Building {}".format(url))
    return url
    


