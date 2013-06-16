#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

A CLI for Everysport.com. 
Lets you print games and standings

'''

import everysport
import argparse


def write_data(league_id, data):
	for d in data.get_all(league_id):
		print d


def main():
	parser = argparse.ArgumentParser(description='Gets games and standings from everysport.com')
	parser.add_argument('-key', '--apikey', action='store',
                   help='Your Everysport APIKEY', dest='apikey')
	parser.add_argument('-t', '--tabell', dest='standings', action='store_true')
	parser.add_argument('-k', '--kommande', dest='upcoming', action='store_true')
	parser.add_argument('-d', '--idag', dest='today', action='store_true')
	parser.add_argument(dest='leagues', metavar='league',nargs='+')
	args = parser.parse_args()


	#Create an API client
	api = everysport.Api(args.apikey)

	for league in args.leagues:
		#Games today
		if args.today:
			write_data(league, api.events().today())
		#Total standings
		if args.standings:
			write_data(league, api.standings().total())
		#Upcoming games
		if args.upcoming:
			write_data(league, api.events().upcoming())
		

if __name__ == '__main__':
	main()