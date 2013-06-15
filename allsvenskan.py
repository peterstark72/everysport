#!/usr/bin/env python
# -*- coding: utf-8 -*-
import everysport

EVERYSPORT_APIKEY = "{APIKEY}"

#Lookup manually at everysport.com
ALLSVENSKAN_2013 = 57973


def main():

	api = everysport.Api(EVERYSPORT_APIKEY)


	allsvenskan_events = api.events().leagues(ALLSVENSKAN_2013)
	allsvenskan_total =  api.standings(ALLSVENSKAN_2013).total()

	#Today's games
	for event in allsvenskan_events.today().load():
			print event
		
	
	#Current standings
	for standing in allsvenskan_total.load():
		print standing


	#Upcoming's games		
	for event in allsvenskan_events.upcoming().load():
			print event



if __name__ == '__main__':
	main()