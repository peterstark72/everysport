Everysport Python 
=================

A Python wrapper for the [Everysport](https://github.com/menmo/everysport-api-documentation) API. The API lets you access events, standings and results from everysport.com. 


## Installation

Using PIP:

```python
pip install everysport
```

Or download and unpack the distribution:

```python
python setup.py install
```


## Basic usage

To start you need an API-key from support@everysport.com. See instructions and usage terms at https://github.com/menmo/everysport-api-documentation.


With the API-key you create an ```Api``` instance. With the Api you can request a league, defined by an Everysport League ID, and start requesting events and standings for the league.

```python
EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

api = everysport.Api(EVERYSPORT_APIKEY)

for event in api.league(everysport.ALLSVENSKAN).events():
    print event

for standing in api.league(everysport.ALLSVENSKAN).standings():
    print standing

```

## Queries

From ```events()``` you get an ```EventsQuery`` that lets you select what kind of events you want to fetch, for example:
- ```today()```
- ```fromdate()```
- ```todate()```
- ```round()```
- ```finished()```
- ```upcoming()```
- ```leagues()```
- ```sport()```

For example: 

```python

football_today = api.events().sport(everysport.FOOTBALL).today()

``` 

To actually fetch the events you can use it as an iterator, as in
```python
for event in football_today:
	print event
```

In the same way you can query for leagues using ```leagues()```.


```python

hockey = api.leagues().sport(everysport.HOCKEY)

for league in hockey:
    print league.name, league.id

```

The leagues are the current leagues, as seen on everysport.com. 











