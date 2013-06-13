import datetime
from models import Event as EventModel


class Event(object):

	def __init__(self, api, id):
		self.api = api
		self.id = id

	def load(self):

		try:
			result = self.api.get_json('events/'+str(self.id))
		except:
			return None

		return EventModel().from_json(result.get('event',{}))	



class Events(object):

	def __init__(self, api):
		self.filter = {}
		self.api = api


	def load(self):
			
		done = False
		while not done:
			try:	
				result = self.api.get_json('events', self.filter)
			except:
				raise StopIteration
			
			count = result['metadata']['count']
			offset = result['metadata']['offset']
			limit = result['metadata']['limit']

			done = count == 0 
			if not done:
				for ev in result.get('events',[]):
					yield EventModel().from_json(ev)
				self.filter['offset'] = offset + count
			done = count < limit


	def fromdate(self, d):
		self.filter['fromDate'] = d
		return self

	
	def todate(self, d):
		self.filter['toDate'] = d
		return self


	def today(self):
		today = datetime.date.today()
		self.filter['toDate'] = self.filter['fromDate'] = today.strftime('%Y-%m-%d')
		return self 


	def status(self, *status):
		self.filter['status'] = ",".join(status)
		return self	


	def leagues(self, *leagues):
		self.filter['league'] = ",".join(map(str, leagues))
		return self


	def sport(self, *sports):
		self.filter['sport'] = ",".join(map(str, sports))
		return self

	def teams(self, *teams):
		self.filter['team'] = ",".join(map(str,teams))
		return self

	













































































