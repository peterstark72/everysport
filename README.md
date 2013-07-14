Everysport Python Module 
=========================

A Python module for [Everysport](https://github.com/menmo/everysport-api-documentation) to access events, standings and results from everysport.com. 


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

```python
EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 

api = everysport.Api(EVERYSPORT_APIKEY)

for event in api.events(everysport.ALLSVENSKAN):
    print event

```









