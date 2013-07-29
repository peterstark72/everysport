#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''season.py

Every League has a Season and each season has diffferent start and end dates.   

'''

import datetime

from commons import Date


class Season(object):
    '''Season

    Properties:
    start - start date
    end - end date

    '''
    def __init__(self, start, end):
        self.start = Date(start)
        self.end = Date(end)

    def __repr__(self):
        return "Season({})".format("-".join(map(repr,[self.start, self.end])))        

    def isactive(self):
        '''Returns True if the season is active today'''
        today = datetime.datetime.today()
        return (today > self.start and today < self.end)





