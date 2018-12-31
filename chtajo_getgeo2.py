#!/usr/bin/env python

import requests
import json
import utm

def getJsonData(id):
    r = requests.get('https://saihtajo.chtajo.es/ajax.php?url=/tr/ajax_datos_tab3/estacion:%s'%id,verify=False,cookies={'idioma':'es'})
    return json.loads(r.text.encode(r.encoding))

def getUtmCoords(id):
    j = getJsonData(id)
    return float(j['cabecera']['UTMX'].replace(',','.')),float(j['cabecera']['UTMY'].replace(',','.')),int(j['cabecera']['HUSO'])

def getGeoCoords(id):
    x,y,h = getUtmCoords(id)
    return utm.to_latlon(x,y,h,'T') # or 'S'

def main():
    f = open('stations_chtajo.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        lat,lon = getGeoCoords(station['id'])
        station['lat'] = lat
        station['lon'] = lon
    f = open('stations_chtajo.json','w')
    json.dump(stations, f)
    f.close()
    #print getGeoCoords('AR42')

if __name__=='__main__':
    main()

