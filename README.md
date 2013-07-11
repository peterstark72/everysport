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


## Basic Usage

Get EVERYSPORT_APIKEY from support@everysport.com.

```python
    api = everysport.Api(EVERYSPORT_APIKEY)


    #Upcoming games in Allsvenskan (swedish football)
    games = api.events().upcoming().leagues(everysport.ALLSVENSKAN)
    for game in games:
        print game


    #Current Allsvenskan Table (standings)
    tables = api.standings(everysport.ALLSVENSKAN).total()        
    for standing in tables:
        print standing


    #Results by team in Allsvenskan
    teams = api.teams(everysport.ALLSVENSKAN)
    games = api.events().upcoming().leagues(everysport.ALLSVENSKAN)
    for res in everysport.stats.results(api, games, *teams):
        print res
```


