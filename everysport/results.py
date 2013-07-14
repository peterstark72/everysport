#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''results.py

'''
from collections import namedtuple


class Result(namedtuple("Result", "team, home, round_, ga, gf, diff, pos, pos_change, against")):

    __slots__ = ()
    def _asjson(self):
        '''Returns a JSON serializable object'''
        return {
            'team' : self.team._asdict(),
            'against': self.against._asdict(),
            'home' : self.home,
            'round' : self.round_,
            'ga' : self.ga,
            'gf' : self.gf,
            'diff' : self.diff,
            'pos' : self.pos,
            'posChange' : self.pos_change
        }



def get_results_for_leagues(api_client, *league_ids):
    '''Generator for Results for given leagues.

    Arguments:
    league_ids - one or many league IDs
    '''

    for league_id in league_ids:
        for event in api_client.events(league_id).finished():

            #Get standings for this round
            standings = api_client.standings(event.league.id).round(event.round).fetchall()
         
            yield Result(
                event.home_team,
                True,
                event.round,
                event.visiting_team_score,
                event.home_team_score,
                event.home_team_score - event.visiting_team_score,
                standings.get_teamposition(event.home_team.id),
                0,
                event.visiting_team)


            #Add visiting team stats

            yield Result(
                event.visiting_team,
                False,
                event.round,
                event.home_team_score,
                event.visiting_team_score,
                event.visiting_team_score - event.home_team_score,
                standings.get_teamposition(event.visiting_team.id),
                0,
                event.home_team)

