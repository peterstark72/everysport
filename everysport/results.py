#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Results domain objects

TeamResultList is a list of TeamResult

TeamResult is a tuple with (team, stats and results),

Resluts is a list of Result.

A Result is a tuple with (pos, events)

'''
from collections import namedtuple 

TeamResult = namedtuple('TeamResult', "team, stats, results")
Result = namedtuple('Result', "pos, events")


class TeamResultList(list):

    def __init__(self, api_client, league_id):
        
        self.events = api_client.events(league_id).finished().fetchall()
        self.standings =  api_client.standings(league_id).fetchall()

        self.rounds = list(set([event.round for event in self.events]))

        self.standings_for_round = {}
        for r in self.rounds:
            self.standings_for_round[r] = api_client.standings(league_id).round(r).fetchall()

       
    def load(self):
        '''Returns Result objects in the order of current standings'''

        for team in self.standings.get_teams():

            #Get stats
            stats = self.standings.get_teamstats(team.id)

            #Get all events for this team
            team_events = self.events.get_events_for_team(team.id)
            
            #Group events by round
            events_by_round = team_events.groupby('round')

            #Get result (pos, event) for every round
            results = []
            for r in reversed(self.rounds):
                pos = self.standings_for_round[r].get_teamposition(team.id)
                events = events_by_round.get(r, [])
                results.append(Result(pos, events))

    
            self.append(TeamResult(team, stats, results)) 
            

        return self









