#!/usr/bin/env python

import requests
from lxml import etree
import utm
import json

def getHtmlTree(url):
    print(url)
    r = requests.get(url)
    return etree.HTML(r.text.encode(r.encoding))

def main():
    stations = []
    for nb in ['ii','iii','iv','v','vi','vii']:
        url = 'http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/subsistema/%s/aforos'%nb
        t = getHtmlTree(url)
        for ficha in t.xpath('//a[starts-with(@href,"http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/ficha/")]/@href'):
            f = getHtmlTree(ficha)
            name,h,x,y,z,town,river,provincia = f.xpath('//td[.="X"]/parent::tr/following::tr/td/text()')[:8]
            river = river.encode('latin1')
            name = name.encode('latin1')
            x = float(x)
            y = float(y)
            h = int(h)
            lat, lon = utm.to_latlon(x,y,h,'S') # all CH is in 29S or 30S
            senales = []
            for grafica in f.xpath('//a[starts-with(@href,"http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/grafica/")]/parent::td/parent::tr'):
                senal1,senal_id,value,unit = grafica.xpath('td/text()')
                try:
                    senal = senal1.encode('latin1')
                    json.dumps(senal)
                except:
                    senal = senal1 # already encoded
                senales.append({'name':senal,'id':senal_id,'unit':unit})
            station_id = ficha.split('/')[-1]
            station = {'id':station_id,'name':name,'utm_x':x,'utm_y':y,'alt':z,'lat':lat,'lon':lon,'river':river,'measures':senales}
            stations.append(station)

    json.dump(stations,open('stations_hidrosur.json','w'))

if __name__=='__main__':
    main()

