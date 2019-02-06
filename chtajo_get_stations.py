#!/usr/bin/env python

import requests
import json

def getStations():
    max_senales = 1000
    url = 'https://saihtajo.chtajo.es/ajax.php?url=/tr/ajax_buscador_senales&max=%d&q=' % max_senales
    r = requests.get(url,verify=False,cookies={'idioma':'es'}) # cookie is mandatory
    t = r.text.encode(r.encoding)
    senales = map(lambda x:x.split('|'),filter(lambda x:len(x)>0,t.split('\n')))
    assert(len(senales)<max_senales)
    for senal in senales:
        id_senal = senal[1]
        url = 'https://saihtajo.chtajo.es/ajax.php?url=/tr/ajax_datos_estacion/estacion:%s' % id_senal
        r = requests.get(url,verify=False,cookies={'idioma':'es'})
        t = r.text.encode(r.encoding)
        try:
            infos = json.loads(t)
        except:
            print('Cannot decode: "%s"' % t)
            infos = {}
        if infos.has_key('contenido') and infos['contenido'].has_key('rio'):
            yield {'id':id_senal,'name':senal[2],'river':infos['contenido']['rio']}
        else:
            print('No rio in %s' % infos)
            yield {'id':id_senal,'name':senal[2]}

def main():
    stations = list(getStations())
    json.dump(stations,open('stations_chtajo.json','w'))

if __name__=='__main__':
    main()
