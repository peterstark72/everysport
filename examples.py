#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import everysport



EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


def main():
    api = everysport.Api(EVERYSPORT_APIKEY)


    #Upcoming games in Allsvenskan (swedish football)
    games = api.events().upcoming().leagues(everysport.ALLSVENSKAN)
    for game in games:
        print game

    #Current Allsvenskan Table (standings)
    tables = api.standings(everysport.ALLSVENSKAN).total()        
    for standing in tables:
        print standing

    #Results by team in Allsvenskan
    teams = api.teams(everysport.ALLSVENSKAN)
    games = api.events().upcoming().leagues(everysport.ALLSVENSKAN)
    for res in everysport.stats.results(api, games, *teams):
        print res


if __name__ == '__main__':
    main()