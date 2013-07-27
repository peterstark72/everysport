#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''edate.py
Everysport Date object.

'''

import datetime



class Date(object):
    '''A Date object for Everysport (swedish) time'''
    
    def __init__(self, s):
        if s and len(s)>16:
            self._date = datetime.datetime.strptime(s[0:16],"%Y-%m-%dT%H:%M" )
        else:
            self._date = None

    def __str__(self):
        if self._date:
            return u"{}".format(self._date.strftime("%Y%m%d"))





