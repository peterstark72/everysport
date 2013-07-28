#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import logging 

import everysport


def main():
    EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

    es = everysport.Everysport(EVERYSPORT_APIKEY)

    allsvenskan = es.getleague(everysport.ALLSVENSKAN)

    print allsvenskan

    print allsvenskan.get_current_round()

    for e in allsvenskan.events:
        print e




if __name__ == '__main__': 
    logging.basicConfig(filename=__file__+'.log', 
                    level=logging.DEBUG, 
                    filemode="w") 
    main()





