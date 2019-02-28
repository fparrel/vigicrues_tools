#!/usr/bin/env python
import json
import os

# add a field to a dict
def add_field(d,f,v):
  d[f] = v
  return d

def getName(station):
  if station.has_key('name'):
     return station['name']
  elif station.has_key('id'):
    return station['id']

def main():
  # Parse all stations
  geos = []
  for fname in filter(lambda x: x.startswith('stations_') and x.endswith('.json'), os.listdir('.')):
    # Extract domain
    domain = fname[9:-5]
    # Parse json file, add domain to all stations, and add it to all stations list
    new_stations = map(lambda x:add_field(x,'domain',domain),json.load(open(fname,'r')))
    # Filter the stations with (lng, lat), and format it into geojson format
    new_geos = map(lambda station: { "type": "Feature", "geometry": { "type": "Point", "coordinates": [station['lon'],station['lat']] }, "properties": {"name":getName(station),"domain":station["domain"]}}, filter(lambda station:station.has_key('lat') and (station.has_key('lng') or station.has_key('lon')),new_stations))
    print('Loading %s, %d stations, %d geos'%(fname,len(new_stations),len(new_geos)))
    geos.extend(new_geos)

  print('Total of geos: %d'%len(geos))
  # Save geojson file to disk
  json.dump({"type": "FeatureCollection", "features": geos }, open('stations.geojson','w'))

  # This file can be viewed for example by http://geojson.tools/

if __name__=='__main__':
  main()

