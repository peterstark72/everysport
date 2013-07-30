#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''season.py

Every League has a Season and each season has diffferent start and end dates.   

'''

from commons import Date


class Season(object):
    '''Season

    Properties:
    start - start date
    end - end date

    '''
    def __init__(self, start, end):
        self._start = Date(start)
        self._end = Date(end)

    def __repr__(self):
        return "Season({})".format("-".join(map(repr,[self.start, self.end])))        

    def ends(self, format="%Y%m%d"):
        '''The date the season ends'''
        if self._end:
            return self._end.strftime(format)


    def starts(self, format="%Y%m%d"):
        '''The date the season starts'''
        if self._start:
            return self._start.strftime(format)





