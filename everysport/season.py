#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''season.py

Every League has a Season and each season has diffferent start and end dates.   

'''

import datetime

from commons import parsedate as parsedate


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
        return "{} - {}".format(self.start.strftime("%Y%m%d"), 
                                self.end.strftime("%Y%m%d"))

    def isactive(self):
        '''Returns True if the season is active today'''
        today = datetime.datetime.today()
        return (today > self.start and today < self.end)

    def timeuntilend(self):
        '''Returns the number of days until the season ends'''
        if self.end:
            return (self.end - datetime.datetime.today()).days



