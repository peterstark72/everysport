#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import everysport



EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


def main():
    api = everysport.Api(EVERYSPORT_APIKEY)
    
    for event in api.events().upcoming().leagues(everysport.ALLSVENSKAN):
        print event


    for standing in api.standings(everysport.ALLSVENSKAN).total():
        print standing


if __name__ == '__main__':
    main()