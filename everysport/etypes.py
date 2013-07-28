#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''etypes.py
Common Everysport data types and functions.

'''

import datetime


def parsedate(date_str):
    '''Parses an Everysport date string. Returns a Python datetime object'''
    if date_str and len(date_str)>16:
        return datetime.datetime.strptime(date_str[0:16],"%Y-%m-%dT%H:%M" )
 



