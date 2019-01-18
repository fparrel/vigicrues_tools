#!/usr/bin/env python
import json
import os

# add a field to a dict
def add_field(d,f,v):
  d[f] = v
  return d

# Parse all stations
stations = []
for fname in filter(lambda x: x.startswith('stations_') and x.endswith('.json'), os.listdir('.')):
  # Extract domain
  domain = fname[9:-5]
  # Parse json file, add domain to all stations, and add it to all stations list
  stations.extend(map(lambda x:add_field(x,'domain',domain),json.load(open(fname,'r'))))
  print 'Loading %s, total %d stations'%(fname,len(stations))

def getlon(station):
  if station.has_key('lng'):
    return station['lng']
  else:
    return station['lon']

# Filter the stations with (lng, lat), and format it into geojson format
out = map(lambda station: { "type": "Feature", "geometry": { "type": "Point", "coordinates": [getlon(station),station['lat']] }, "properties": {"name":station["id"],"domain":station["domain"]}}, filter(lambda station:station.has_key('lat') and (station.has_key('lng') or station.has_key('lon')),stations))
# Save geojson file to disk
json.dump({"type": "FeatureCollection", "features": out }, open('stations.geojson','w'))

# This file can be viewed for example by http://geojson.tools/

