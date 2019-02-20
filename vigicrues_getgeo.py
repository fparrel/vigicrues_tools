#!/usr/bin/env python

import json
from sandre import getLatLonFromSandreId

def loadStations():
    f = open('stations_vigicrues.json','r')
    stations = json.load(f)
    f.close()
    return stations

def main():
    stations = loadStations()
    for station in stations:
        station_id = station['id'][:-2]
        print station_id
        lat, lon = getLatLonFromSandreId(station_id)
        if lat!=None and lon!=None:
            station['lat'] = lat
            station['lon'] = lon

    f = open('stations_vigicrues.json','w')
    json.dump(stations,f)
    f.close()

if __name__=='__main__':
    main()

