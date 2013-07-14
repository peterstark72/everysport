#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport



EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


def main():

    api = everysport.Api(EVERYSPORT_APIKEY)

    standings = api.standings(everysport.ALLSVENSKAN).total().fetchall()        
    allsvenskan = standings.group()        

    for teamstats in allsvenskan.standings:
        print teamstats.team.name.encode('utf-8')
        print teamstats.stats.__dict__




if __name__ == '__main__':
    main()