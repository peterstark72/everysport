#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport



EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


def main():

    api = everysport.Api(EVERYSPORT_APIKEY)

    games = api.events(everysport.ALLSVENSKAN).upcoming()

    for game in games.getall():
        print game



if __name__ == '__main__':
    main()