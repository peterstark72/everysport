
#Used to parse RFC822 datetime string
from dateutil.parser import parse

class Team(object):

	def __init__(self, 
		id=None,
		link=None,
		name=None,
		short_name=None):
		self._id = id
		self._link = link
		self._name = name
		self._short_name = short_name


	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, x):
		self._id = x 


	@property
	def link(self):
		return self._link

	@link.setter
	def link(self, x):
		self._link = x 		


	@property
	def name(self):
		return self._name.encode('utf-8')

	@name.setter
	def name(self, x):
		self._name = x 

	@property
	def short_name(self):
		return self._short_name

	@short_name.setter
	def short_name(self, x):
		self._short_name = x 


	def from_json(self, data):
		return Team(id=data.get('id', None),
					name=data.get('name', None),
					link=data.get('link', None),
					short_name=data.get('shortName', None))



class Sport(object):

	def __init__(self, 
		id=None,
		name=None):
		self._id = id
		self._name = name


	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, x):
		self._id = x 

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, x):
		self._name = x 

	def from_json(self, data):
		return Sport(id=data.get('id', None),
					name=data.get('name', None))

class Arena(object):

	def __init__(self, 
		id=None,
		name=None):
		self._id = id
		self._name = name


	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, x):
		self._id = x 

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, x):
		self._name = x 

	def from_json(self, data):
		return Arena(id=data.get('id', None),
					name=data.get('name', None))

class League(object):

	def __init__(self, 
		id=None,
		name=None,
		sport=None,
		team_class=None):
		self._id = id
		self._name = name
		self._sport = sport
		self._team_class = team_class


	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, x):
		self._id = x 

	@property
	def name(self):
		return self._name.encode('utf-8')

	@name.setter
	def name(self, x):
		self._name = x 

	@property
	def sport(self):
		return self._sport

	@sport.setter
	def sport(self, x):
		self._sport = x 		

	@property
	def team_class(self):
		return self._team_class


	def from_json(self, data):
		if 'sport' in data: 
			sport = Sport().from_json(data['sport'])
		else: 
			sport = None
		return League(id=data.get('id', None),
					name=data.get('name', None),
					sport=sport,
					team_class=data.get('teamClass',None))




class Event(object):

	def __init__(self, 
		start_date=None,
		round=None,
		status=None,
		home_team=None,
		visiting_team=None,
		home_team_score=None,
		visiting_team_score=None,
		league=None,
		arena=None,
		spectators=None,
		referees=None):
		self._start_date = start_date
		self._round = round
		self._status = status
		self._home_team = home_team
		self._visiting_team = visiting_team
		self._home_team_score=home_team_score
		self._visiting_team_score=visiting_team_score
		self._league = league
		self._arena=arena	
		self._spectators=spectators
		self._referees=referees


	@property
	def start_date(self):
		return parse(self._start_date)

	@property
	def round(self):
		return self._round


	@property
	def status(self):
		'''The status of the event'''
		return self._status


	def is_finished(self):
		return self._status == "FINISHED"


	@property
	def home_team(self):
		return self._home_team


	@property
	def visiting_team(self):
		return self._visiting_team

	@property
	def home_team_score(self):
		return self._home_team_score

	@property
	def visiting_team_score(self):
		return self._visiting_team_score


	@property
	def league(self):
		return self._league


	@property
	def arena(self):
		return self._arena

	@property
	def spectators(self):
		return self._spectators

	@property
	def referees(self):
		return self._referees


	def from_json(self, data):

		if 'homeTeam' in data:			
			home_team = Team().from_json(data['homeTeam'])
		else:
			home_team = None

		if 'visitingTeam' in data:	
			visiting_team = Team().from_json(data['visitingTeam'])
		else:
			visiting_team = None
		
		if 'league' in data:
			league = League().from_json(data['league'])	
		else:
			league = None


		if 'facts' in data:
			if 'arena' in data['facts']:
				arena = Arena().from_json(data['facts']['arena'])
			else:
				arena = None
			spectators = data['facts'].get('spectators', None)
			referees = data['facts'].get('referees', None)
		else:
			arena = None
			spectators = None
			referees = None


		return Event(start_date=data.get('startDate',None),
				status=data.get('status',None),
				round=data.get('round',None),
				home_team=home_team,
				visiting_team=visiting_team,
				home_team_score=data.get('homeTeamScore',None),
				visiting_team_score=data.get('visitingTeamScore',None),
				league=league,
				arena=arena,
				spectators=spectators,
				referees=referees
			)



def main():

	ev = Event()
	print ev.status
	ev.status = "Upcoming"
	print ev.status

	print ev.start_date


if __name__ == '__main__':
	main()

