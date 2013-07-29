#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''commons.py
Common Everysport classes and function.

'''

import datetime

class Date(datetime.datetime):
    '''Everysport Date object. Timezone is always CEST and it's created from the Everysport API Date format'''
    def __new__(cls, data):
        if data and len(data)>16:
            d = datetime.datetime.strptime(data[0:16],"%Y-%m-%dT%H:%M" )
            return datetime.datetime.__new__(cls, d.year, d.month, d.day, d.hour, d.minute)

    def __repr__(self):
        return "Date({})".format(self.strftime("%Y%m%d"))


