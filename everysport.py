#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import json
import datetime


EVERYSPORT_API_URL = "http://api.everysport.com/v1/{}"



def get_resource(resource, params):
	'''Makes a GET with defines params and returns result or None'''

	encoded_params = urllib.urlencode(params)
	url = EVERYSPORT_API_URL.format(resource) + '?' + encoded_params
	try:
		response = urllib.urlopen(url)
		result = json.load(response)
	except IOError:
		return None
	
	return result



def get_list(resource, params):	
	'''Generator, loads all events '''

	done = False
	while not done:			
		result = get_resource(resource, params)
		count = result['metadata']['count']
		offset = result['metadata']['offset']
		limit = result['metadata']['limit']

		done = count == 0 
		if not done:
			for event in result.get(resource,[]):
				yield event
			params['offset'] = offset + count
		done = count < limit




class Endpoint(object):

	def __init__(self, apikey):
		self.params = {}
		self.params['apikey'] = apikey		

	def limit(self, limit):
		self.params['limit'] = limit
		return self



class Events(Endpoint):

	def fromdate(self, d):
		self.params['fromDate'] = d
		return self

	
	def todate(self, d):
		self.params['toDate'] = d
		return self


	def today(self):
		today = datetime.date.today()
		self.params['toDate'] = self.params['fromDate'] = today.strftime('%Y-%m-%d')
		return self 


	def status(self, *status):
		self.params['status'] = ",".join(status)
		return self	


	def leagues(self, *leagues):
		self.params['league'] = ",".join(map(str, leagues))
		return self


	def sport(self, *sports):
		self.params['sport'] = ",".join(map(str, sports))
		return self


	def load(self):	
		return get_list('events', self.params)

			
class Sports(Endpoint):

	def load(self):	
		return get_list('sports', self.params)



class Leagues(Endpoint):

	def team_class(self, *team_classes):
		self.params['sport'] = ",".join(map(str, team_classes))
		return self


	def sport(self, *sports):
		self.params['sport'] = ",".join(map(str, sports))
		return self

	def load(self):	
		return get_list('leagues', self.params)













































































