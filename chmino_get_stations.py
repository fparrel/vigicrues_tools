#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import utm
import json

def main():
    r = requests.get('http://saih.chminosil.es/index.php?url=/datos/mapas/mapa:H1/area:HID/acc:',cookies={'lang':'es'})
    #r = requests.get('http://saih.chminosil.es/index.php?url=/datos/mapas/mapa:H1/area:HID/acc:1')
    html = r.text.encode(r.encoding)
    tree = etree.HTML(html)
    patficha = re.compile(r'index\.php\?url=/datos/ficha/estacion:([A-Z_0-9]+)/area:([A-Z_0-9]+)')
    fichas = map(lambda e:patficha.findall(e.get('href'))[0],tree.xpath('//*[starts-with(@href,"index.php?url=/datos/ficha")]'))
    patgrafica = re.compile(r'index\.php\?url=/datos/graficas/tag:([A-Z_0-9]+)')
    graficas = map(lambda e:patgrafica.findall(e.get('href'))[0],tree.xpath('//*[starts-with(@href,"index.php?url=/datos/graficas")]'))
    print(graficas)
    stations = []

    for ficha in fichas:
        print(ficha)
        station_id = ficha[0]
        rf = requests.get('http://saih.chminosil.es/index.php?url=/datos/ficha/estacion:%s/area%s'%ficha,cookies={'lang':'es'})
        htmlf = rf.text.encode(rf.encoding)
        tree = etree.HTML(htmlf)
        h,x,y,z = tree.xpath('//th[.="Coordenadas UTM:"]/parent::tr/following::tr[1]/td')
        h = int(h.text)
        x = float(x.text)
        y = float(y.text)
        z = float(z.text)
        lat,lon = utm.to_latlon(x,y,h,'T')
        name = tree.xpath('//td[.="Nombre:"]/following::td[1]')[0].text
        river = tree.xpath(u'//td[.="Río:"]/following::td[1]')[0].text
        tags = []
        for grafica in graficas:
            if grafica.startswith(station_id):
                tags.append(grafica)
        station = {'lat':lat,'lon':lon,'id':station_id,'name':name,'river':river,'tags':tags}        
        print(station)
        stations.append(station)

    json.dump(stations, open('stations_chmino.json','w'))

if __name__=='__main__':
    main()

