#!/usr/bin/env python
# -*- coding: utf-8 -*-
import everysport


EVERYSPORT_APIKEY = "{APIKEY}"
ALLSVENSKAN_2013 = 57973


def main():

	api = everysport.Api(EVERYSPORT_APIKEY)

	allsvenskan_games = api.events().leagues(ALLSVENSKAN_2013)

	for event in allsvenskan_games.status('UPCOMING').all():
		print event



if __name__ == '__main__':
	main()