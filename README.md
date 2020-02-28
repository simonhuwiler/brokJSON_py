# BrokJSON
Ever struggled with huge GeoJSON-Files? BrokJSON is your space-saving alternative! Depending on your data you can save up to 80%. **Withouth losing any data!** Why? Because it uses the same ideas as GeoJSON.
  
The idea behind BrokJSON: **RAM is mightier than the bandwidth** - download the small BrokJSON and convert it on runtime to GeoJSON than loading a huge GeoJSON.

## Example
This **GeoJSON** with just two Points...
```json
{
  "type": "FeatureCollection",
  "features": [
  {
    "type": "Feature",
    "properties": {
      "id": 1,
      "title": "Datapoint 1",
      "value": 343
    },
    "geometry": {
      "type": "Point",
      "coordinates": [8.5402,47.3782]
    }
  },
  {
    "type": "Feature",
    "properties": {
      "id": 1,
      "title": "Datapoint 2",
      "value": 14
    },
    "geometry": {
      "type": "Point",
      "coordinates": [8.5637,47.4504]
    }
  }]
}
```
... looks as a **BrokJSON** like this:

```json
{
  "properties": ["id", "title", "value"],
  "geometries": [{
    "type": "Point",
    "features": [
      [[8.5402, 47.3782], [1, "Datapoint 1", 343]],
      [[8.5637, 47.4504], [1, "Datapoint 2", 14]]
    ]
  }
]}
```
No information lost, everything is there. Amazing!


## Installation
```console
pip install brokjson
```

## Usage
```python
# import BrokJSON
import brokjson

# Load your GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [8.5402,47.3782]
        }
    }]
}

# Convert your Json-Object to BrokJson
brok = brokjson.geo2brok(geojson);

# "brok" is your BrokJSON as a dictionary object
print(brok)

# Convert it back
geojson = brokjson.brok2geo(brok)
print(geojson)
```


## Documentation
BrokJSON is a lightweight library, there are only two functions.
### GeoJSON to BrokJSON
```python
brokjson.geo2brok(geoJsonObject)
```
**Parameters**  
`GeoJSON` as a `Dictionary`

**Return value**  
`BrokJSON` as a `Dictionary`

### BrokJSON to GeoJSON
```python
brokjson.brok2geo(brokJsonObject)
```
**Parameters**  
`BrokJSON` as a `Dictionary`

**Return value**  
`GeoJSON` as a `Dictionary`

## Full Spec and other languages
Have a look at https://www.brokjson.dev