#!/usr/bin/env python

import json
import requests
import datetime
from serialize import save_values

def loadStations():
    f = open('stations_chj.json', 'r')
    stations = json.load(f)
    f.close()
    return stations

def main():
    for station in loadStations():
        print(station['id'])
        ps = 24*60/5+3
        url = 'http://saih.chj.es/chj/saih/stats/datosGrafico?v=%s&t=ultimos5minutales&%d=30' % (station['var'],ps)
        print(url)
        r = requests.get(url)
        values = list(filter(lambda dv:dv[1]!=None,map(lambda dv:(datetime.datetime.strptime(dv[0],'%d/%m/%Y %H:%M'),dv[1]),r.json()[1])))
        if len(values)>0:
            save_values('chj',station['id'],values)

if __name__=='__main__':
    main()
