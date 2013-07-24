#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''event.py


'''


from league import League
from commons import Team, Facts, Date


class Event(object):
    '''Everysport Event'''

    def __init__(self, 
            api_client=None,
            id=None,
            start_date=None,
            round_=None,
            status=None,
            home_team=None,
            visiting_team=None,
            home_team_score=None,
            visiting_team_score=None,
            finished_time_status=None,
            league=None,
            facts=None):
        self.api_client=api_client
        self.id=id
        self._start_date=start_date
        self.round=round_
        self.home_team=home_team
        self.visiting_team=visiting_team
        self.home_team_score=home_team_score
        self.visiting_team_score=visiting_team_score
        self.finished_time_status=finished_time_status
        self.league=league
        self.facts=facts

    @classmethod
    def from_dict(cls, api_client, data):
        return cls(
                api_client,
                data.get('id', None),
                data.get('startDate', None),
                data.get('round',None),
                data.get('status',None),
                Team.from_dict(data.get('homeTeam',{})),
                Team.from_dict(data.get('visitingTeam',{})),
                data.get('homeTeamScore',None),
                data.get('visitingTeamScore',None),
                data.get('finishedTimeStatus',None),
                League.from_dict(api_client, data.get('league',{})),
                Facts.from_dict(data.get('facts', {}))
            )

    @classmethod
    def find(cls, api_client, event_id):
        endpoint = 'events/' + str(event_id)
        data = api_client._fetchresource(endpoint)
        return cls.from_dict(api_client, data.get('event', {}))

    @property        
    def start_date(self):
        if self._start_date:
            return Date.from_str(self._start_date)
            #return parsedate(self._start_date)


    def __str__(self):
        return u"{} {}, {} - {}".format(self.id, self.start_date.strftime("%Y%m%d"), self.home_team.name, self.visiting_team.name).encode('utf-8')

