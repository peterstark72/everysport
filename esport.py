#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

A CLI for Everysport.com. 
Lets you print games and standings


'''
import argparse

import everysport


#Try to get APIKEY from OS env
import os
try: 
	APIKEY = os.environ['EVERYSPORT_APIKEY']
except KeyError:
	APIKEY = ""


def main():
	parser = argparse.ArgumentParser(description='Gets games and standings from everysport.com')	
	parser.add_argument('-key', '--apikey', action='store',
                   help='Your Everysport APIKEY', dest='apikey', nargs="?", default=APIKEY)
	parser.add_argument('-s', '--standings', dest='standings', action='store_true')
	parser.add_argument('-u', '--upcoming', dest='upcoming', action='store_true')
	parser.add_argument('-r', '--results', dest='results', action='store_true')	
	parser.add_argument('-t', '--today', dest='today', action='store_true')
	parser.add_argument( dest='leagues', nargs='+')
	

	args = parser.parse_args()


	#Create an API client
	api = everysport.Api(args.apikey)
	events = api.events()

	if args.today:
		games = events.today().leagues(*args.leagues)
		everysport.writers.write_events(games)

	if args.results:
		games = events.finished().leagues(*args.leagues)
		everysport.writers.write_events(games)				

	if args.upcoming:
		games = events.upcoming().leagues(*args.leagues)
		everysport.writers.write_events(games)				


	#Total standings
	if args.standings:
		stdns = api.standings().total().league(args.leagues[0]).load()
		everysport.writers.write_tables(stdns)

	

if __name__ == '__main__':
	main()