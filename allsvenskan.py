#!/usr/bin/env python
# -*- coding: utf-8 -*-

import everysport


#The Everysport APIKEY is inside a JSON object in 'config.json': 
#{"APIKEY" : {YOUR APIKEY}, "ALLSVENSKAN_LEAGUE_ID" : 57973 }  
import json
config = json.load(open('config.json'))


def main():

	api = everysport.Api(config['APIKEY'])

	allsvenskan_games = api.events().leagues(config['ALLSVENSKAN_LEAGUE_ID'])

	for game in allsvenskan_games.load():
		print game.start_date.strftime('%d/%m %H:%M').rjust(10),
		print "{}-{}".format(game.home_team.name, game.visiting_team.name),

		if game.arena:
			print ", {} ({})".format(game.arena.name.encode('utf-8'), game.spectators),

		if game.is_finished():
			print ", {}-{}".format(game.home_team_score,game.visiting_team_score),

		print 	




if __name__ == '__main__':
	main()
