Everysport API Python 
=====================

A Python wrapper for the [Everysport API](https://github.com/menmo/everysport-api-documentation). 


Example usage:


```python
api = everysport.Api(EVERYSPORT_APIKEY)


allsvenskan_events = api.events().leagues(ALLSVENSKAN_2013)
allsvenskan_total =  api.standings(ALLSVENSKAN_2013).total()

#Today's games
for event in allsvenskan_events.today().load():
		print event
	

#Current standings
for standing in allsvenskan_total.load():
	print standing


#Upcoming's games		
for event in allsvenskan_events.upcoming().load():
		print event	
```



