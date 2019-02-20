#!/usr/bin/env python

# wget http://www.chguadiana.es/Geoportal/Carto/ESTCONTROL_es040_EPSG25830.zip --no-check-certificate
# unzip ESTCONTROL_es040_EPSG25830.zip
# ogr2ogr -f geojson SaihEstControl.geojson SaihEstControl.shp

import json

#f = open('RC_AF.geojson','r')
f = open('SaihEstControl.geojson','r')
geojson = json.load(f)
f.close()

f = open('stations_chguadiana.json','r')
stations = json.load(f)
f.close()

for station in stations:
    station_id = station['id']
    found = False
    for feature in geojson['features']:
        if feature['properties']['CODIGO'] == station_id:
        #if feature.has_key('properties') and feature['properties'].has_key('DESC_OBSER') and feature['properties']['DESC_OBSER']!=None and station_id in feature['properties']['DESC_OBSER']:
            station['lat'] = feature['properties']['GEOG_LAT']
            station['lon'] = feature['properties']['GEOG_LONG']
            found = True
    print 'Station: %s found: %s'%(station_id,found)

f = open('stations_chguadiana.json','w')
json.dump(stations,f)
f.close()

