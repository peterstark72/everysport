Everysport Python 
=================

A Python wrapper for the [Everysport](https://github.com/menmo/everysport-api-documentation) API. The API lets you access events, standings and results from [everysport.com](http://everysport.com). 


## Installation

Using PIP:

```python
pip install everysport
```

Or download and unpack the distribution:

```python
python setup.py install
```


## Getting Started

To start you need an API-key from support@everysport.com. See instructions and usage terms at https://github.com/menmo/everysport-api-documentation.


With the API-key you create an ```Api``` instance. With the Api you can request a league, defined by an Everysport League ID, and start requesting events and standings for the league.

```python
APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(APIKEY)
```


## Getting League Standings

To get standings for a league, you need to first get the league by League ID (as on everysport.com) or, for current leagues, by name and sport: 

```python 

#By name of current league
allsvenskan = es.getleague_by_name("Allsvenskan", "football")
nhl = es.getleague_by_name("NHL", "hockey")

#By League ID from everysport.com
shl = es.getleague(60243)
```

Once you have the league, you get standings in the following ways: 

```python

print allsvenskan.totals
print allsvenskan.home
print allsvenskan.away

print allsvenskan.round(7).totals
```

Leagues like NHL, which has many different groups, are more complicated: 

```python

for group_type in nhl.standings.grouptypes(): # e.g. 'conference'
    
    for group in nhl.standings.groups(group_type): 
        print group.upper()
    
        for standings in nhl.standings.group(group):
            print standings 
```


## Queries

Create queries to get list of leagues and events. There are two types of queries: 

- ```everysport.events```
- ```everysport.leagues```

From ```events``` you get query object that lets you select what kind of events you want to fetch, for example:
- ```today()```
- ```fromdate()```
- ```todate()```
- ```round()```
- ```finished()```
- ```upcoming()```
- ```leagues()```
- To filter a specific sport, you can use ```football()```, ```hockey()```, etc.

For example: 

```python

football_today = es.events.football().today()

``` 

To fetch the events, use the query as an iterator, as in
```python
for event in football_today:
	print event
```

Or use ```fetch``` to get all back as one list (not recommended, the number of events may be large for some leagues):

```python
all_hockey = es.events.leagues(everysport.SHL, everysport.NHL).fetch()
```

In the same way you can query for leagues using ```leagues```.


```python

for league in es.leagues.hockey():
    print league

```

The leagues are the current leagues, as seen on everysport.com. 


















