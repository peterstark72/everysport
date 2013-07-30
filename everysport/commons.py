#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''commons.py
Common Everysport classes and function.

'''

import datetime
from collections import namedtuple


class Date(datetime.datetime):
    '''Everysport Date object. Timezone is always CEST and it's created from the Everysport API Date format'''
    def __new__(cls, data):
        if data and len(data)>16:
            d = datetime.datetime.strptime(data[0:16],"%Y-%m-%dT%H:%M" )
            return datetime.datetime.__new__(cls, d.year, d.month, d.day, d.hour, d.minute)

    def __repr__(self):
        return "Date({})".format(self.strftime("%Y%m%d"))



class SportName(namedtuple('SportName', "fullname shortname abbr")):
    '''A SportName such as a team, league'''
    __slots__ = ()

    def __repr__(self):
        return self.fullname.encode('utf-8')




if __name__ == '__main__':
    
    n = u"Djurgården"     
    print repr(n)
    print n.encode('utf-8')
    #print n #does not work


    sn = SportName(n, None, None)
    print sn
    print sn.abbr
    #print sn.name #Does not work

