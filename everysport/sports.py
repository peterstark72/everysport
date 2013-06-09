from models import Sport

class Sports(object):
	def __init__(self, api):
		self.api = api
		self.filter = {}


	def load(self):
			
		done = False
		while not done:
			try:	
				result = self.api.get_json('sports', self.filter)
			except:
				raise StopIteration
			
			count = result['metadata']['count']
			offset = result['metadata']['offset']
			limit = result['metadata']['limit']

			done = count == 0 
			if not done:
				for league in result.get('sports',[]):
					yield Sport().from_json(league)
				self.filter['offset'] = offset + count
			done = count < limit


