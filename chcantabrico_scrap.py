#!/usr/bin/env python

import json
import requests
import datetime
from serialize import save_values
from chcantabrico_get_stations import getFlow4Level

def getStations():
    f = open('stations_chcantabrico.json', 'r')
    stations = json.load(f)
    f.close()
    return stations

def parseLine(line):
    d,v=line.split(';')
    return datetime.datetime.strptime(d,"%d/%m/%Y %H:%M:%S"),float(v)

def main():
    flow4level_updated = False
    stations = getStations()
    for station in stations:
        print station['id']
        url = 'https://www.chcantabrico.es/evolucion-de-niveles/-/descarga/csv/nivel/%s' % station['id']
        r = requests.get(url)
        csv = r.text.encode(r.encoding)
        lines = csv.split('\n')[2:]
        values = map(parseLine,filter(lambda line: line.strip()!='',lines))
        if len(values)>0:
            save_values('chcantabrico','nivel_%s'%station['id'],values)
        flow4level = getFlow4Level(station['url'])
        len_bf = len(station['flow4level'])
        station['flow4level'].update(flow4level) #update `station` dict in place with new value(s)
        if len(station['flow4level'])>len_bf:
            flow4level_updated = True

    if flow4level_updated:
        print 'New value got for flow4level'
        json.dump(stations,open('stations_chcantabrico.json','w'))

if __name__=='__main__':
    main()
