#!/usr/bin/env python

from arpapiemonte_get_stations import getData
from serialize import loadStations, saveValues
import datetime

def main():
    stations = loadStations('arpapiemonte')
    for station in stations:
        d = getData(station['url'])
        if len(d)>0:
            saveValues('arpapiemonte',station['station_id'],filter(lambda dv:dv[1]!=None,map(lambda dv: (datetime.datetime.fromtimestamp(dv[0]/1000.0),dv[1]),d['data'])))

if __name__=='__main__':
    main()

