#!/usr/bin/env python

import requests
import yaml
import json

def main():
    r = requests.get('http://www.saihduero.es/risr')
    t = r.text.encode(r.encoding)
    i = t.find('datosAF =')
    i = t.find('{',i)
    j = t.find(');',i)
    datos = '['+t[i:j].replace('\t','')+']'
    print datos
    stations = yaml.load(datos)
    # Replace lng by lon in order to be coherent with stations from other sources
    for station in stations:
        station['lon'] = station['lng']
        del station['lng']
    json.dump(stations,open('stations_chduero.json','w'))

if __name__=='__main__':
    main()

