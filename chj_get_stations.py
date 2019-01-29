#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def main():
    r = requests.get('http://saih.chj.es/chj/saih/glayer/listaEstaciones?t=a&id=')
    stations = []
    for s in r.json():
        if s['unidades'] == u'm³/s':
            station = {'id':s['id'],'lat':s['latitud'],'lon':s['longitud'],'name':s['nombre'],'var':s['variable']}
            stations.append(station)

    json.dump(stations,open('stations_chj.json','w'))

if __name__=='__main__':
    main()
