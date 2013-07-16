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

        self.number_of_rounds = max([event.round for event in self.events])

        self.standings_for_round = []
        for r in range(self.number_of_rounds):
            self.standings_for_round.append(api_client.standings(league_id).round(r+1).fetchall())


    def get_events_for_team(self, team_id):
        '''Returns the list of events where the team is home- or visiting''' 
        return [e for e in self.events if team_id in (e.home_team.id, e.visiting_team.id)]


    def group_events_by_round(self, events):        
        events_by_round = {}
        for e in events:
            events_by_round[e.round] = e
        return events_by_round
    

       
    def load(self):
        '''Returns Result objects in the order of current standings'''

        for team in self.standings.get_teams():

            result = {}                
            result['team'] = team
            result['stats'] = self.standings.get_teamstats(team.id).__dict__

            team_events = self.get_events_for_team(team.id)

            events_by_round = self.group_events_by_round(team_events)

            result['results'] = []
            for r in reversed(range(len(self.standings_for_round))):
                pos = self.standings_for_round[r].get_teamposition(team.id)
                ev = events_by_round.get(r+1, None)

                if not ev:
                    result['results'].append({'pos': pos, 'event': None})
                elif team.id == ev.home_team.id:
                    result['results'].append({'pos': pos, 'event': Result(ev.home_team_score, ev.visiting_team_score, ev.visiting_team.name)._asdict()})
                else:
                    result['results'].append({'pos': pos, 'event': Result(ev.visiting_team_score, ev.home_team_score, ev.home_team.name)._asdict()})


            self.append(result)

        return self


