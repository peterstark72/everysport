#!/usr/bin/python
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
	parser.add_argument('-r', '--results', dest='results', action='store_true')	
	parser.add_argument('-t', '--today', dest='today', action='store_true')
	parser.add_argument('-l', '--leagues', dest='leagues', nargs='+')
	parser.add_argument('-e', '--events', dest='events', nargs='+')
	args = parser.parse_args()

	#Create an API client
	api = everysport.Api(args.apikey)

	
	#Get list of leagues, if provided
	if args.leagues:
		leagues = args.leagues
	else:
		leagues = []	

	for league in leagues:
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

		#Results
		if args.results:
			for d in api.events().finished().get_all(league):
				print d	


		#Upcoming games
		if args.upcoming:
			for d in api.events().upcoming().get_all(league):
				print d	

	
	#Get events
	if args.events:
		events = args.events 	
	else:
		events = []	
				
	#Traverse events and print					
	for event in events:
		ev = api.events().get(event)
		print ev		

	

if __name__ == '__main__':
	main()