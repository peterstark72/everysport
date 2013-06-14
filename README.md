Everysport API Python 
=====================

A Python wrapper for the [Everysport API](https://github.com/menmo/everysport-api-documentation). 


Example usage:


```python
import everysport

EVERYSPORT_APIKEY = {APIKEY}

#Lookup manually at everysport.com
ALLSVENSKAN_2013 = 57973


def main():

	api = everysport.Api(EVERYSPORT_APIKEY)

	allsvenskan_games = api.events().leagues(ALLSVENSKAN_2013)

	for event in allsvenskan_games.upcoming().all():
		print event



if __name__ == '__main__':
	main()
	
```



