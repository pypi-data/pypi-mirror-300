PyMoot
======

PyMoot is a python wrapper to retrieve data from komoot or change some data on Komoot.

Features
--------

- Get all your tours
- Get a specific tour by ID
- Retrieve tour GPX file
- Retrieve tour coordinates
- Rename a tour on komoot
- Get tour highlights

Install
-------

PyMoot requires python >= 3.11

To install, it's easy:

```bash
pip install pymoot
```

Usage
-----

First initialize the connector:

```python
from pymoot.connector import Connector

c = Connector(email="myemail@example.com", password="komoot_password")
```

Then, use the function that you cant from this connector:

```python
from pymoot.connector import Connector

c = Connector(email="myemail@example.com", password="komoot_password")

# Call what you want here:
c.get_tours()  # Get tours
tour = c.get_tour(tour_id="125431322")  # Get a tour by id
c.update_tour_title(tour_identifier="213135132", new_title="New title to set")  # Update title of a tour on Komoot
tour.retrieve_gpx()  # Get tour GPX
tour.retrieve_coordinates()  # Get tour coordinates
tour.retrieve_tour_highlights()  # Get tour highlights
```
