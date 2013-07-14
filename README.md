Everysport Python Module 
=========================

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

You need an EVERYSPORT_APIKEY from support@everysport.com, then you create an Api instance and start requesting events and standings.

Here is how you print all events in Allsvenskan (swedish football):

```python
EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

api = everysport.Api(EVERYSPORT_APIKEY)

for event in api.events(everysport.ALLSVENSKAN):
    print event

```

The events() call returns an EventsQuery that lets you select what kind of events you want to fetch, for example:
- today()
- fromdate()
- todate()
- round()
- finished()
- upcoming()

For example: 

```python
api.events(everysport.ALLSVENSKAN).finished().today()
``` 

To actually fetch the events you can simply use it as an iterator, as in
```python
for event in api.events(everysport.ALLSVENSKAN):
	print event
```

In this case you get one event at a time, and save memory. 

Or call ```fetchall()``` to load all events into a one list.
```python
events = api.events(everysport.ALLSVENSKAN).fetchall() #200+ events in one list
```

If you want events for more than one league, just add more into the events() call: 
```python
swe_elite_football = api.events(everysport.ALLSVENSKAN, everysport.SUPERETTAN)

for event in swe_elite_football:
	print event
```


## Standings

A league consist of one or many groups; for example, the different Conferences in NHL. Most leagues, however, have just one group. 

When you call standings(), you get a StandingsQuery on which you can call:
- total()
- home()
- away()
- round()

Call fetchall() to fetch the selected standings. 

```
EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

api = everysport.Api(EVERYSPORT_APIKEY)

standings = api.standings(everysport.ALLSVENSKAN).total().fetchall() 

allsvenskan = standings.group()        

for teamstats in allsvenskan.standings:
    print teamstats

```












