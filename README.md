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


## Basic usage

To start you need an API-key from support@everysport.com. See instructions and usage terms at https://github.com/menmo/everysport-api-documentation.


With the API-key you create an ```Api``` instance. With the Api you can request a league, defined by an Everysport League ID, and start requesting events and standings for the league.

```python
EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

es = everysport.Everysport(EVERYSPORT_APIKEY)

for event in es.getleague(everysport.ALLSVENSKAN).events():
    print event

for standing in es.league(everysport.ALLSVENSKAN).standings():
    print standing

```

## Queries

From ```events``` you get query object that lets you select what kind of events you want to fetch, for example:
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

football_today = es.events.sport("Football").today()

``` 

To fetch the events, use the query as an iterator, as in
```python
for event in football_today:
	print event
```

Or use ```fetch``` to get all back as one list (not recommended, the number of events may be large for some leagues):

```python
all_hockey = es.events.sport("Hockey").leagues(everysport.SHL, everysport.NHL).fetch()
```

In the same way you can query for leagues using ```leagues```.


```python

hockey = es.leagues.sport("Hockey")

for league in hockey:
    print league

```

The leagues are the current leagues, as seen on everysport.com. 


## Leagues

Leagues on Everysport are identified with a League ID, that can be looked up at everysport.com site, or by using the ```leagues``` query. 

Here are som League IDs for common leagues:

```
#Football
ALLSVENSKAN = 57973
SUPERETTAN = 57974

#Hockey
SHL = 60243
NHL = 58878
```

You access a league in the following way: 
```python
shl = es.league(everysport.SHL)
```

Once you have the league you can start working with events:

```python

for event in sorted(shl.events, key = lambda e:e.hometeam.name):
    print event
```

And with standings:

```python

nhl = es.league(everysport.NHL).standings

print nhl #Complete league, all teams


for g in nhl.groups(): 
    print g 


for g in nhl.groups('conference'): 
    print g #Conferences


print nhl.group("Western Conference")

```


















