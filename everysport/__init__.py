#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import Api, EverysportException
import results

'''Teams from everysport.com
'''

from teams import Team 

MFF = Team(9375,u"Malmö FF", "", "")
HBG = Team(9373,u"Helingsborgs IF", "", "")
LSD = Team(1175,u"Leksand", "", "")
CHI = Team(28075,u"Chicago Blackhawks", "", "")



'''
	ID for everysport.com sports, as defined by 

	http://api.everysport.com/v1/sports


'''
AMERICAN_FOOTBALL = 18 #swedish: amerikansk fotboll
BADMINTON = 9
BANDY = 3
BASEBALL = 20
BASKET = 5
TABLE_TENNIS = 8
BOWLING = 1
WRESTLING = 16 #swedish: brottning
FOOTBALL = 10
HANDBALL = 7
FLOORBALL = 4
HOCKEY = 2
RUGBY = 17
SOFTBALL = 68
SPEEDWAY = 15
SQUASH = 22
TENNIS = 19
VOLLEYBALL = 11




'''
	Leagues
'''
#Football
ALLSVENSKAN = 57973
SUPERETTAN = 57974

#Hockey
SWISS_LEAGUE = 58882
SHL = 60243
NHL = 58878



