#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''season.py

Everysport teams are defined with an ID. They always have a name, and may also have a short name and an abbreviation.


'''

import datetime

from etypes import parsedate as parsedate


class Season(object):
    '''Season

    Properties:
    start - start date
    end - end date

    '''
    def __init__(self, start, end):
        self.start = parsedate(start)
        self.end = parsedate(end)

    def __str__(self):
        return "{} - {}".format(self.start, self.end)

    def isactive(self):
        '''Returns True of the season is active today'''
        today = datetime.datetime.today()
        return (today > self.start and today < self.end)

    def timeuntilend(self):
        '''Returns the timedelta until the season ends'''
        if self.end:
            return (self.end - datetime.datetime.today()).days



