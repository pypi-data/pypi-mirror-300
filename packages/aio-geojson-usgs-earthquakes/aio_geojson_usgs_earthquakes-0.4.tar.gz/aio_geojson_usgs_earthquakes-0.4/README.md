# python-aio-geojson-usgs-earthquakes

[![Build Status](https://img.shields.io/github/actions/workflow/status/exxamalte/python-aio-geojson-usgs-earthquakes/ci.yaml)](https://github.com/exxamalte/python-aio-geojson-usgs-earthquakes/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/exxamalte/python-aio-geojson-usgs-earthquakes/branch/main/graph/badge.svg?token=91DC4HHZQJ)](https://codecov.io/gh/exxamalte/python-aio-geojson-usgs-earthquakes)
[![PyPi](https://img.shields.io/pypi/v/aio-geojson-usgs-earthquakes.svg)](https://pypi.python.org/pypi/aio-geojson-usgs-earthquakes)
[![Version](https://img.shields.io/pypi/pyversions/aio-geojson-usgs-earthquakes.svg)](https://pypi.python.org/pypi/aio-geojson-usgs-earthquakes)

This library provides convenient async access to U.S. Geological Survey Earthquake Hazards Program feeds.
 
## Installation
`pip install aio-geojson-usgs-earthquakes`

## Usage
See below for examples of how this library can be used. After instantiating a 
particular class - feed or feed manager - and supply the required parameters, 
you can call `update` to retrieve the feed data. The return value 
will be a tuple of a status code and the actual data in the form of a list of 
feed entries specific to the selected feed.

Status Codes
* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

**Parameters**

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |

**Supported Feeds**

| Category                               | Feed                                 |
|----------------------------------------|--------------------------------------|
| Past Hour - Significant Earthquakes    | `past_hour_significant_earthquakes`  |
| Past Hour - M4.5+ Earthquakes          | `past_hour_m45_earthquakes`          |
| Past Hour - M2.5+ Earthquakes          | `past_hour_m25_earthquakes`          |
| Past Hour - M1.0+ Earthquakes          | `past_hour_m10_earthquakes`          |
| Past Hour - All Earthquakes            | `past_hour_all_earthquakes`          |
| Past Day - Significant Earthquakes     | `past_day_significant_earthquakes`   |
| Past Day - M4.5+ Earthquakes           | `past_day_m45_earthquakes`           |
| Past Day - M2.5+ Earthquakes           | `past_day_m25_earthquakes`           |
| Past Day - M1.0+ Earthquakes           | `past_day_m10_earthquakes`           |
| Past Day - All Earthquakes             | `past_day_all_earthquakes`           |
| Past 7 Days - Significant Earthquakes  | `past_week_significant_earthquakes`  |
| Past 7 Days - M4.5+ Earthquakes        | `past_week_m45_earthquakes`          |
| Past 7 Days - M2.5+ Earthquakes        | `past_week_m25_earthquakes`          |
| Past 7 Days - M1.0+ Earthquakes        | `past_week_m10_earthquakes`          |
| Past 7 Days - All Earthquakes          | `past_week_all_earthquakes`          |
| Past 30 Days - Significant Earthquakes | `past_month_significant_earthquakes` |
| Past 30 Days - M4.5+ Earthquakes       | `past_month_m45_earthquakes`         |
| Past 30 Days - M2.5+ Earthquakes       | `past_month_m25_earthquakes`         |
| Past 30 Days - M1.0+ Earthquakes       | `past_month_m10_earthquakes`         |
| Past 30 Days - All Earthquakes         | `past_month_all_earthquakes`         |

**Supported Filters**

| Filter            |                            | Description |
|-------------------|----------------------------|-------------|
| Radius            | `filter_radius`            | Radius in kilometers around the home coordinates in which events from feed are included. |
| Minimum Magnitude | `filter_minimum_magnitude` | Minimum magnitude as float value. Only event with a magnitude equal or above this value are included. |


**Example**
```python
import asyncio
from aiohttp import ClientSession
from aio_geojson_usgs_earthquakes import UsgsEarthquakeHazardsProgramFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: 21.3, Longitude: -157.8
        # Feed: Past Day - All Earthquakes
        # Filter radius: 500 km
        # Filter minimum magnitude: 4.0
        feed = UsgsEarthquakeHazardsProgramFeed(websession,
                                                (21.3, -157.8),
                                                'past_day_all_earthquakes',
                                                filter_radius=5000, 
                                                filter_minimum_magnitude=4.0)
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```

## Feed entry properties
Each feed entry is populated with the following properties:

| Name               | Description                                                                                         | Feed attribute |
|--------------------|-----------------------------------------------------------------------------------------------------|----------------|
| geometries         | All geometry details of this entry.                                                                 | `geometry`     |
| coordinates        | Best coordinates (latitude, longitude) of this entry.                                               | `geometry`     |
| distance_to_home   | Distance in km of this entry to the home coordinates.                                               | n/a            |
| attribution        | Attribution of the feed.                                                                            | n/a            |
| external_id        | The unique public identifier for this entry.                                                        | `id`           |
| title              | Title of this entry.                                                                                | `title`        |
| place              | Description of the place where this earthquakes occurred.                                           | `place`        |
| magnitude          | Magnitude of this earthquake.                                                                       | `mag`          |
| time               | Date and time when this event occurred.                                                             | `time`         |
| updated            | Date and time when this entry was last updated.                                                     | `updated`      |
| alert              | Alert level of this entry ("green", "yellow", "orange", "red").                                     | `alert`        |
| type               | Type of this seismic event ("earthquake", "quarry").                                                | `type`         |
| status             | Indicates whether the event has been reviewed by a human ("automatic", "reviewed", "deleted").      | `status`       |


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest 
  timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
