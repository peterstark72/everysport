#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport



EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


def main():

    api = everysport.Api(EVERYSPORT_APIKEY)

    standings = api.standings(everysport.ALLSVENSKAN).total()        
    for standings_group in standings.getall():
        print standings_group

            


    #List of teams in Allsvenskan and Superettan
    teams = api.get_teams(everysport.ALLSVENSKAN, everysport.SUPERETTAN)

    for team in teams:
        print team.name.encode('utf-8')


if __name__ == '__main__':
    main()