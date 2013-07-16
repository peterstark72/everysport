#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''results.py

'''
from collections import namedtuple 


Result = namedtuple('Results', "gf, ga, against")


class Results(list):
    '''Generates''' 

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

            result = {}                
            result['team'] = team
            result['stats'] = self.standings.get_teamstats(team.id).__dict__

            team_events = self.events.get_events_for_team(team.id)

            events_by_round = team_events.groupby_rounds()

            result['results'] = []
            for r in reversed(self.rounds):

                pos = self.standings_for_round[r].get_teamposition(team.id)
                
                events = events_by_round.get(r, None)

                result['results'].append({'pos': pos, 'events': events})

            self.append(result)

        return self


