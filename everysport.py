#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

A CLI for Everysport.com. 
Lets you print games and standings

'''

import everysport
import argparse


def main():
	parser = argparse.ArgumentParser(description='Gets games and standings from everysport.com')
	parser.add_argument('-key', '--apikey', action='store',
                   help='Your Everysport APIKEY', dest='apikey')
	parser.add_argument('-s', '--standings', dest='standings', action='store_true')
	parser.add_argument('-u', '--upcoming', dest='upcoming', action='store_true')
	parser.add_argument('-t', '--today', dest='today', action='store_true')
	parser.add_argument(dest='leagues', metavar='league',nargs='+')
	args = parser.parse_args()


	#Create an API client
	api = everysport.Api(args.apikey)

	for league in args.leagues:
		#Games today
		if args.today:
			for d in api.events().today().get_all(league):
				print d	

		#Total standings
		if args.standings:
			for group in api.standings().total().get(league):
				for label in group.labels:
					print label.name,
				print
				for s in group.standings:
					print s


		#Upcoming games
		if args.upcoming:
			for d in api.events().upcoming().get_all(league):
				print d	

		

if __name__ == '__main__':
	main()