#!/usr/bin/env python
# -*- coding: utf-8 -*-

subcuencas = {0: "Mijares - Palancia",1: "Júcar Medio",2: "Vinalopó - Marina",3: "Serpis",4: "Bajo Júcar",5: "Bajo Turia",6: "Alto Turia",7: "Alto Júcar",8: "Maestrazgo"}

rios = {(39.608212,-0.474241):"Barranc del Carraixet",(40.467724,0.301524):"Rambla de Cervera",(40.087381,-0.558316):"Río Mijares",(38.725132,-2.224348):"Río Casas de Lázaro",(39.628212,-0.663970):"Rambla Castellana",(39.476864,-1.117889):"Río Magro",(40.614192,-0.976151):"Río Alfambra"}

import requests
import json
import pymongo
from math import sin,cos,atan2,sqrt

c = pymongo.MongoClient()
rivers = list(c['wwsupdb']['osm'].find({},{'paths':True}))

def GeodeticDistGreatCircle(lat1,lon1,lat2,lon2):
    "Compute distance between two points of the earth geoid (approximated to a sphere)"
    # convert inputs in degrees to radians
    lat1 = lat1 * 0.0174532925199433
    lon1 = lon1 * 0.0174532925199433
    lat2 = lat2 * 0.0174532925199433
    lon2 = lon2 * 0.0174532925199433
    # just draw a schema of two points on a sphere and two radius and you'll understand
    a = sin((lat2 - lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1)/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    # earth mean radius is 6371 km
    return 6372795.0 * c

def findRiver(lat,lon):
    for latlon,name in rios.iteritems():
        if GeodeticDistGreatCircle(lat,lon,latlon[0],latlon[1])<10.0:
            return name
    m = None
    rid = None
    for river in rivers:
        for path in river['paths']:
            for pt in path:
                d = GeodeticDistGreatCircle(lat,lon,pt[0],pt[1])
                if m==None or d<m:
                    m = d
                    rid = river['_id']
                #if d<200.0:
                #    return river['_id']
    #print 'min=%f'%m
    if m<700.0:
        return rid
    return None

def main():
    r = requests.get('http://saih.chj.es/chj/saih/glayer/listaEstaciones?t=a&id=')
    stations = []
    for s in r.json():
        if s['unidades'] == u'm³/s':
            station = {'id':s['id'],'lat':s['latitud'],'lon':s['longitud'],'name':s['nombre'],'var':s['variable'],'unit':'m3/s','subcuenca':subcuencas[s['subcuenca']]}
            river = findRiver(station['lat'],station['lon'])
            if river!=None:
                station['river'] = river
            else:
                print 'River not found at %f,%f'%(station['lat'],station['lon'])
            stations.append(station)

    json.dump(stations,open('stations_chj.json','w'))

if __name__=='__main__':
    main()

