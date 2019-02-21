#!/usr/bin/env python

import json
from sandre import getLatLonFromSandreId
from serialize import loadStations

def main():
    stations = loadStations('vigicrues')
    for station in stations:
        station_id = station['id'][:-2]
        print(station_id)
        lat, lon = getLatLonFromSandreId(station_id)
        if lat!=None and lon!=None:
            station['lat'] = lat
            station['lon'] = lon

    f = open('stations_vigicrues.json','w')
    json.dump(stations,f)
    f.close()

if __name__=='__main__':
    main()

