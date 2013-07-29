#!/usr/bin/env python

import hashlib 

_cache = {}


def add(key, data):
    _cache[key] = data


def addurl(url, data):
    key = hashlib.md5(url).hexdigest()
    return add(key, data)


def get(key):
    if key in _cache:
        return _cache[key]


def geturl(url):
    key = hashlib.md5(url).hexdigest()
    return get(key)