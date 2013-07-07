Everysport API Python 
=====================

A Python wrapper for the [Everysport API](https://github.com/menmo/everysport-api-documentation). 


## Installation


Using PIP:

```python
pip install everysport
```

Or download and unpack the distribution:

```python
python setup.py install
```



## Usage

Create the API client, with your APIKEY from support@everysport.com

```python
api = everysport.Api(EVERYSPORT_APIKEY)
```

Create a few queries:

```python

ALLSVENSKAN = 57973

allsvenskan_today = api.events().today().leagues(ALLSVENSKAN)

allsvenskan_standings = api.standings().total().league(ALLSVENSKAN)

allsvenskan_upcoming = api.events().upcoming().leagues(ALLSVENSKAN)
```

Get data and print:
```python

#Today's games
everysport.writers.write_events(allsvenskan_today)


#Upcoming's games		
everysport.writers.write_events(allsvenskan_upcoming)


#Standnings
everysport.writers.write_table(allsvenskan_standings)
```



