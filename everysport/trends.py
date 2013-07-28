#!/usr/bin/env python
# -*- coding: utf-8 -*-




def positiontrend(api_client, league):


    trend = []
    
    for team in league.teamlist:
        team_trend = {}
        team_trend['stats'] = league.standings.getstats(team)
        team_trend['result'] = []
        for r in league.roundslist:
            result = {}
            standings_for_round = league.round(r).standings
            result['pos'] = standings_for_round.getteamposition(team)
            team_trend['result'].append(result)
        trend.append(team_trend)
    
    return trend