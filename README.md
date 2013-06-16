Everysport API Python 
=====================

A Python wrapper for the [Everysport API](https://github.com/menmo/everysport-api-documentation). 


Create the API client, with your APIKEY from supper@everysport.com

```python
api = everysport.Api(EVERYSPORT_APIKEY)
```

Create a few queries:

```python

events_today = api.events().today()

standings_total = api.standings().total()

upcoming_events = api.events().upcoming()
```

Get the data by specifying League ID from everysport.com (Allsvenskan is 57973):
```python

ALLSVENSKAN = 57973

#Today's games
for event in events_today.get_all(ALLSVENSKAN):
		print event
	

#Current standings
for standing in standings_total.get_all(ALLSVENSKAN):
	print standing


#Upcoming's games		
for event in upcoming_events.get_all(ALLSVENSKAN):
		print event	
```



