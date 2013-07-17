#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Encodes ResultsList as JSON strings


'''
import datetime
import json


class DatetimeEncoder(json.JSONEncoder):
    '''Encodes dates as 2013-11-11 16:16'''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M")
        return json.JSONEncoder.default(self, obj)



def json_dumps(results):
    '''Takes a ResultList and returns a JSON string'''

    arr = []
    for teamresult in results:

        team_id = teamresult.team.id
        
        d = {}
        d['team'] = {
                'name' : teamresult.team.name, 
                'id' : teamresult.team.id 
                }
        
        d['stats'] = teamresult.stats.__dict__

        def decode_result(result):
            '''Result is pos, events'''
            r = {}
            r['pos'] = result.pos
            if len(result.events) < 1:
                r['event'] = None
            else:
                ev = result.events[0] #Assume never >1 event / round
                if ev.home_team.id == team_id:
                    r['event'] = {'gf' : ev.home_team_score, 
                                'ga': ev.visiting_team_score, 'against': ev.visiting_team.name}
                else:
                    r['event'] = {'gf' : ev.visiting_team_score, 
                                'ga': ev.home_team_score, 'against': ev.home_team.name}
            return r
            

        d['results'] = map(decode_result, teamresult.results)
        
        arr.append(d)


    return json.dumps(arr, cls=DatetimeEncoder)