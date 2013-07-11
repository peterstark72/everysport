#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''results.py


'''

import logging

from collections import namedtuple

GameResult = namedtuple("GameResult", "team, round, ga, gf, diff, pos, pos_change, against")


def get_position_for_round(standings, team_id, round_):
	'''Returns position for a team in a given round

	Arguments:
	round_ - the round for which to get position
	team_id - the Team ID from everysport.com
	'''

	#Find team position
	for group in standings.round(round_):
		for pos, teamstats in enumerate(group.standings):
			if teamstats.team.id == team_id:
				return pos+1


def get_position_change(standings, team_id, from_round, to_round):
	'''Returns the position change from prevuous to given round

	Arguments:
	round_ - The round for which to get change
	team_id - The Team ID from everysport.com

	''' 

	if from_round < 1 or to_round < 1:
		return 0

	if from_round == to_round:
		return 0

	pos_from = get_position_for_round(standings, team_id, from_round)
	pos_to = get_position_for_round(standings, team_id, to_round)
	
	return pos_from - pos_to


class ResultsList(list):
	'''List of event stats '''  

	def __init__(self, api_client, events):

		for event in events.finished():

			standings = api_client.standings(event.league.id)

			#Add home team stats
			self.append(GameResult(
				event.home_team,
				event.round,
				event.visiting_team_score,
				event.home_team_score,
				event.home_team_score - event.visiting_team_score,
				get_position_for_round(standings, 
					event.home_team.id, 
					event.round),
				get_position_change(standings, 
					event.home_team.id, 
					event.round-1,
					event.round),
				event.visiting_team))

			#Add visiting team stats
			self.append(GameResult(
				event.visiting_team,
				event.round,
				event.home_team_score,
				event.visiting_team_score,
				event.visiting_team_score - event.home_team_score,
				get_position_for_round(standings, 
						event.visiting_team.id,
						event.round),
				get_position_change(standings, 
					event.visiting_team.id, 
					event.round-1,
					event.round),
				event.home_team))



def results(api_client, events, *teams):
	'''Returns for each given team a list of game results based on the given events. 

	Arguments:
	api_client - Everysport API api_client
	events - list of everysport events
	*team_ids - one or many teams for which to get results
	'''

	all_results = ResultsList(api_client, events)
	logging.debug("All results {}".format(all_results))

	results_by_team = [] 
	for team in teams:
		results = [res for res in all_results if res.team.id == team.id ]
		logging.debug("Results for {} : {}".format(team.id, results))
		results_by_team.append(results)
	
	return results_by_team


