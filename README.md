Everysport Python 
=================

A Python wrapper for the [Everysport](https://github.com/menmo/everysport-api-documentation) API. The API lets you access events, standings and results from [everysport.com](http://everysport.com). 

Note: This is NOT an official Everysport SDK and is subject to change at any time. 


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


With the API-key you create an ```Everysport``` instance. 

```python
APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(APIKEY)
```


## Getting a specific League 

To get a specific league, you need the League ID from everysport.com: Navigate to the league page on eversport.com, the League ID is in the URL. This is the URL for Allsvenskan:

http://www.everysport.com/sport/fotboll/fotbollsserier-2013/allsvenskan-herr/allsvenskan/57973

The League ID for Allsvenskan is 57973. 

```python 
allsvenskan = es.get_league(57973) # Allsvenskan

print allsvenskan.league

```

Leagues like NHL, which has many different groups, are more complicated: 

```python

nhl = es.get_standings(58878)

for group_type in nhl.grouptypes: # e.g. 'conference'
    print group_type.upper()    
    for group_name in nhl.get_groupnames_by_type(group_type):         
        print nhl.get_group_by_name(group_name)

```

Note that the League ID is different for every season! 

## Queries

Create queries to get list of leagues and events. There are two types of queries: 

- ```everysport.events```
- ```everysport.leagues```

From ```events``` you get query object that lets you select what kind of events you want to fetch, for example:

- ```today()```
- ```ongoing()```
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

The leagues are the current leagues, as seen on everysport.com!

 


















