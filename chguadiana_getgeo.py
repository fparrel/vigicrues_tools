#!/usr/bin/env python

# wget http://www.chguadiana.es/Geoportal/Carto/ESTCONTROL_es040_EPSG25830.zip --no-check-certificate
# unzip ESTCONTROL_es040_EPSG25830.zip
# ogr2ogr -f geojson SaihEstControl.geojson SaihEstControl.shp

import json

def main():

    # Load GIS data
    f = open('SaihEstControl.geojson','r')
    geojson = json.load(f)
    f.close()

    # Load stations
    f = open('stations_chguadiana.json','r')
    stations = json.load(f)
    f.close()

    # For each station, search into GIS data and update `stations`
    for station in stations:
        station_id = station['id']
        found = False
        for feature in geojson['features']:
            if feature['properties']['CODIGO'] == station_id:
                station['lat'] = feature['properties']['GEOG_LAT']
                station['lon'] = feature['properties']['GEOG_LONG']
                found = True
                break
        print('Station: %s found: %s'%(station_id,found))

    # Save stations
    f = open('stations_chguadiana.json','w')
    json.dump(stations,f)
    f.close()

if __name__=='__main__':
    main()

