Everysport API Python 
=====================

A Python wrapper for the [Everysport API](https://github.com/menmo/everysport-api-documentation). 


Example usage:


```python
import everysport

api = everysport.Api(EVERYSPORT_APIKEY)

allsvenskan_games = api.events().leagues(57973)

for game in allsvenskan_games.load():
	print game.start_date.strftime('%d/%m %H:%M')
	print game.home_team.name, game.visiting_team.name 
	
```



