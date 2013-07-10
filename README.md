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
    
    for event in api.events().upcoming().leagues(everysport.ALLSVENSKAN):
        print event


    for standing in api.standings(everysport.ALLSVENSKAN).total():
        print standing
```


