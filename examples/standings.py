#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import logging 

import everysport


def main():
    EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

    es = everysport.Everysport(EVERYSPORT_APIKEY)

    
    allsvenskan = es.getleague_by_name("Allsvenskan", "Football")

    #nhl = es.getleague_by_name("NHL", "Hockey")

    print allsvenskan.totals

    print allsvenskan.getpositiontrends()


    


if __name__ == '__main__': 
    logging.basicConfig(filename=__file__+'.log', 
                    level=logging.DEBUG, 
                    filemode="w") 
    main()





