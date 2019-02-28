#!/usr/bin/env python
# -*- coding: utf-8 -*-

subcuencas = {0: "Mijares - Palancia",1: "Júcar Medio",2: "Vinalopó - Marina",3: "Serpis",4: "Bajo Júcar",5: "Bajo Turia",6: "Alto Turia",7: "Alto Júcar",8: "Maestrazgo"}

rios = {(39.608212,-0.474241):"Barranc del Carraixet",(40.467724,0.301524):"Rambla de Cervera",(40.087381,-0.558316):"Río Mijares",(38.725132,-2.224348):"Río Casas de Lázaro",(39.628212,-0.663970):"Rambla Castellana",(39.476864,-1.117889):"Río Magro",(40.614192,-0.976151):"Río Alfambra"}

import requests
import json
from riverfromdb import findRiver

def main():
    r = requests.get('http://saih.chj.es/chj/saih/glayer/listaEstaciones?t=a&id=')
    stations = []
    for s in r.json():
        if s['unidades'] == u'm³/s':
            station = {'id':s['id'],'lat':s['latitud'],'lon':s['longitud'],'name':s['nombre'],'var':s['variable'],'unit':'m3/s','subcuenca':subcuencas[s['subcuenca']]}
            river = findRiver(station['lat'],station['lon'],rios)
            if river!=None:
                station['river'] = river
            else:
                print 'River not found at %f,%f'%(station['lat'],station['lon'])
            stations.append(station)

    json.dump(stations,open('stations_chj.json','w'))

if __name__=='__main__':
    main()

