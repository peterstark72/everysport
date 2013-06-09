import events
import leagues
import sports
import urllib
import json

BASE_API_URL = "http://api.everysport.com/v1/{}"

class Api(object):
	def __init__(self, apikey):
		self.params = {}
		self.params['apikey'] = apikey

	def events(self):
		return events.Events(self)

	def leagues(self):
		return leagues.Leagues(self)		

	def sports(self):
		return sports.Sports(self)	

	def event(self, id):
		return events.Event(self, id)

	def get_json(self, endpoint, params=dict()):
		self.params.update(params)
		encoded_params = urllib.urlencode(self.params)
		url = BASE_API_URL.format(endpoint) + '?' + encoded_params	
		response = urllib.urlopen(url)
		return json.load(response)







