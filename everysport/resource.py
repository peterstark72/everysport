#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import logging
import hashlib
import json


cache = {}

def getresource(url):
    '''Returns the resource at the url. '''

    #Check if already in cache, else add it
    key = hashlib.md5(url).hexdigest()
    if key not in cache:
        logging.info("Loading {}".format(url))
        response = urllib2.urlopen(url)
        cache[key] = json.load(response)

    return cache[key]