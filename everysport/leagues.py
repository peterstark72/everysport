from models import League

class Leagues(object):

	def __init__(self, api):
		self.api = api
		self.filter = {}

	def load(self):
			
		done = False
		while not done:
			try:	
				result = self.api.get_json('leagues', self.filter)
			except:
				raise StopIteration
			
			count = result['metadata']['count']
			offset = result['metadata']['offset']
			limit = result['metadata']['limit']

			done = count == 0 
			if not done:
				for league in result.get('leagues',[]):
					yield League().from_json(league)
				self.filter['offset'] = offset + count
			done = count < limit

	def team_class(self, *team_classes):
		self.filter['teamClass'] = ",".join(map(str, team_classes))
		return self


	def sport(self, *sports):
		self.filter['sport'] = ",".join(map(str, sports))
		return self
