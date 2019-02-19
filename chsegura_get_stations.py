#!/usr/bin/env python

import requests
from lxml import etree
import utm
import json
import re

url = 'http://www.saihsegura.es/apps/ivisor/cauces3.php?tipo=0'
r = requests.get(url)
html = r.text.encode(r.encoding)
tree = etree.HTML(html)
findstations = re.compile(r'[0-9A-Z]{5}Q[0-9]{2}')
puntos2 = map(lambda s:s[0],filter(lambda s:len(s)>0,map(lambda s:findstations.findall(s), tree.xpath('//a/@title'))))
#puntos2 = map(lambda s:findstations.findall(s),tree.xpath('//div[@class="cauce_mapa_container"]/@title'))
#puntos2 = [item for sublist in puntos2 for item in sublist]
puntos2 = list(set(puntos2))
print puntos2
#exit()

stations = []
for zona in ['I','II','III','IV','V','VI','VII','VIII']:
    url = 'http://www.saihsegura.es/apps/ivisor/fichas3.php?zona=%s' % zona
    r = requests.get(url)
    html_zona = r.text.encode(r.encoding)
    tree_zona = etree.HTML(html_zona)
    for a in tree_zona.xpath('//a'):
        punto = a.get('href').lstrip("javascript:set_punto('").rstrip("');")
        name = a.text
        url = 'http://www.saihsegura.es/apps/ivisor/fichas2.php?punto=%s' % punto
        r = requests.get(url)
        html = r.text.encode(r.encoding)
        tree = etree.HTML(html)
        name = tree.xpath('//font[@style="font-size:26px"]/text()')[0].strip()
        huso,x,y,z = map(str.strip,tree.xpath('//b[.="Huso"]/parent::td/parent::tr/following::tr[1]/td/text()'))
        river = tree.xpath('//b[.="Cauce"]/parent::td/following::td[1]/text()')[0].strip()
        l = huso[-1]
        h = int(huso[:-1])
        x = int(x)
        y = int(y)
        lat,lon = utm.to_latlon(x,y,h,l)
        #url = 'http://www.saihsegura.es/apps/ivisor/estadisticas.php?punto=%s' % punto
        #r = requests.get(url)
        #html = r.text.encode(r.encoding)
        #tree = etree.HTML(html)
        #linkstats = tree.xpath('//a')
        #punto2 = linkstats[0].get('href').lstrip("javascript:set_punto_medicion('").rstrip("')")
        #print 'punto2="%s"'%punto2
        #url = 'http://www.saihsegura.es/apps/ivisor/estadisticas2.php'
        #r = requests.post(url,{'punto':punto2},cookies={'SAIHSESSIONID':'2bbe61befa9044bb37bc9fc4bb88b78f7ff9a8cd09cc7fbc0f0e9dc4e0b685633addd0c18edfcb401b626cc5c6507aff60b9a2caeff6567beceb5030a79a54b4E4EF20C7'})
        #html = r.text.encode(r.encoding)
        #print html
        #tree = etree.HTML(html)
        #print tree.xpath("//font[color='#0000CC']")
        #exit()
        puntos2_of_station = []
        for p in puntos2:
            if p.startswith(punto):
                puntos2_of_station.append(p)
        station = {'id': punto, 'name': name, 'utm_h': huso, 'utm_x': x, 'utm_y': y, 'alt': z, 'river': river, 'lat': lat, 'lon':   lon  , 'ids': puntos2_of_station}
        print station
        if len(puntos2_of_station)>0:
            stations.append(station)

json.dump(stations,open('stations_chsegura.json','w'))

