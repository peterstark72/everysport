#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

	stats.py

'''

import logging



class EventStats(object):
	''''''

	def __init__(self, api_client, league_id, *team_ids):
		self.league_id = league_id

		logging.info("Creating stats for {} in {}".format(team_ids,league_id))

		self.standings = api_client.standings(league_id)
		self.events = api_client.events().finished().leagues(league_id)

		if len(team_ids) > 0:
			self.events = self.events.teams(*team_ids)


	def get_team_position_by_round(self, round_, team_id):
		'''Returns position for a team in a given round

		Arguments:
		round_ - the round for which to get position
		team_id - the Team ID from everysport.com
		'''

		#Get standings for given round
		league_standings = self.standings.round(round_)	

		#Find team position
		for group in league_standings:
			for pos, teamstats in enumerate(group.standings):
				if teamstats.team.id == team_id:
					return pos+1


	def get_position_change(self, round_, team_id):
		'''Returns the position change from prevuous to given round

		Arguments:
		round_ - The round for which to get change
		team_id - The Team ID from everysport.com
		''' 
		if round_ <= 1:
			return 0
		curr_pos = self.get_team_position_by_round(round_, team_id)
		prev_pos = self.get_team_position_by_round(round_-1, team_id)
		return prev_pos-curr_pos


	def trend(self):

		matrix = {}
		for event in self.events:

			#Add teams to matrix,
			if event.home_team.name not in matrix:
					matrix[event.home_team.name] = []
			if event.visiting_team.name not in matrix:
					matrix[event.visiting_team.name] = []


			#Get stats and append	
			#ga,gf,against,diff,round,pos,pos_change
			stats = {}
			stats['ga'] = event.visiting_team_score
			stats['gf'] = event.home_team_score
			stats['diff'] = stats['gf'] - stats['ga']
			stats['against'] = event.visiting_team._asdict()
			stats['round'] = event.round
			stats['pos'] = self.get_team_position_by_round(event.round, event.home_team.id)
			stats['posChange'] = self.get_position_change(event.round,event.home_team.id)
			matrix[event.home_team.name].append(stats)

			stats = {}
			stats['ga'] = event.home_team_score
			stats['gf'] = event.visiting_team_score
			stats['diff'] = stats['gf'] - stats['ga']
			stats['against'] = event.home_team._asdict()
			stats['round'] = event.round
			stats['pos'] = self.get_team_position_by_round(event.round, event.visiting_team.id)
			stats['posChange'] = self.get_position_change(event.round,event.visiting_team.id)
			matrix[event.visiting_team.name].append(stats)


		return matrix


