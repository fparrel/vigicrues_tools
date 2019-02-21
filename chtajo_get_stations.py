#!/usr/bin/env python

import requests
import json
import utm

def getJsonData(station_id):
    r = requests.get('https://saihtajo.chtajo.es/ajax.php?url=/tr/ajax_datos_tab3/estacion:%s'%station_id,verify=False,cookies={'idioma':'es'})
    return json.loads(r.text.encode(r.encoding))

def getUtmCoords(station_id):
    j = getJsonData(station_id)
    return float(j['cabecera']['UTMX'].replace(',','.')),float(j['cabecera']['UTMY'].replace(',','.')),int(j['cabecera']['HUSO'])

def getGeoCoords(station_id):
    x,y,h = getUtmCoords(station_id)
    return utm.to_latlon(x,y,h,'T') # or 'S'?

def getStations():
    max_senales = 1000
    url = 'https://saihtajo.chtajo.es/ajax.php?url=/tr/ajax_buscador_senales&max=%d&q=' % max_senales
    print(url)
    r = requests.get(url,verify=False,cookies={'idioma':'es'}) # cookie is mandatory
    t = r.text.encode(r.encoding)
    stations = map(lambda x:x.split('|'),filter(lambda x:len(x)>0,t.split('\n')))
    assert(len(stations)<max_senales)
    for station_split in stations:
        station_id = station_split[1]
        lat, lon = getGeoCoords(station_id)
        url = 'https://saihtajo.chtajo.es/ajax.php?url=/tr/ajax_datos_estacion/estacion:%s' % station_id
        print(url)
        r = requests.get(url,verify=False,cookies={'idioma':'es'})
        t = r.text.encode(r.encoding)
        infos = json.loads(t)['contenido']
        river = infos['rio']
        for senal in infos['datos_tr']:
             tag = senal['tag']
             desc = senal['descripcion']
             unit = senal['unidad']
             station = {'senal_id': tag, 'station_id': station_id, 'name': station_split[2], 'desc': desc, 'unit': unit, 'river': river, 'lat': lat, 'lon': lon}
             yield station
#        station = {'id':id_senal,'name':senal[2]}
#        if infos.has_key('contenido') and infos['contenido'].has_key('rio'):
#            station['river'] = infos['contenido']['rio']
#        else:
#            print('WARNING: No rio in %s' % infos)
#        yield station

def main():
    stations = list(getStations())
    json.dump(stations,open('stations_chtajo.json','w'))

if __name__=='__main__':
    main()

