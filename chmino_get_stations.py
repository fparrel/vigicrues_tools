#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import utm
import json

def main():

    # Get map of the whole C.H.
    url = 'http://saih.chminosil.es/index.php?url=/datos/mapas/mapa:H1/area:HID/acc:'
    print(url)
    r = requests.get(url,cookies={'lang':'es'})
    html = r.text.encode(r.encoding)

    # Parse all 'fichas' (link to station description)
    tree = etree.HTML(html)
    patficha = re.compile(r'index\.php\?url=/datos/ficha/estacion:([A-Z_0-9]+)/area:([A-Z_0-9]+)')
    fichas = map(lambda e:patficha.findall(e.get('href'))[0],tree.xpath('//*[starts-with(@href,"index.php?url=/datos/ficha")]'))

    # Remove doubloons
    fichas = list(set(list(fichas)))

    # Prepare 'grafica' parsing
    patgrafica = re.compile(r'index\.php\?url=/datos/graficas/tag:([A-Z_0-9]+)')

    # Build stations array
    stations = []

    for ficha in fichas:

        # Get 'ficha'
        station_id, area = ficha
        url = 'http://saih.chminosil.es/index.php?url=/datos/ficha/estacion:%s/area%s'%ficha
        print(url)
        rf = requests.get(url,cookies={'lang':'es'}) # Cookie is mandatory
        htmlf = rf.text.encode(rf.encoding)
        treef = etree.HTML(htmlf)

        # Parse coordenates
        h, x, y, z = treef.xpath('//th[.="Coordenadas UTM:"]/parent::tr/following::tr[1]/td')
        h = int(h.text)
        x = float(x.text)
        y = float(y.text)
        z = float(z.text)
        lat, lon = utm.to_latlon(x,y,h,'T')

        # Parse station name and river name
        name = treef.xpath('//td[.="Nombre:"]/following::td[1]')[0].text
        river = treef.xpath(u'//td[.="Río:"]/following::td[1]')[0].text

        # For each measure(=senal=tag) of station add an item
        for tr in treef.xpath('//a[@class="icono_grafica"]/parent::td[1]/parent::tr[1]'):
            desc = tr.xpath('td/text()')[0] # Description of measure
            unit = tr.xpath('td/text()')[4] # Unit (m, m3/s...)
            url = tr.xpath('td/a/@href')[0] # url without domain name
            tag = patgrafica.findall(url)[0] # Extract measure id from url
            station = { 'lat': lat, 'lon': lon, 'station_id': station_id, 'name': name, 'river': river, 'alt': z,\
                   'utm_x': x, 'utm_y': y, 'utm_h': h, 'senal_id': tag, 'desc': desc, 'unit': unit, \
                   'url':'http://saih.chminosil.es/%s' % url, 'station_area': area }
            stations.append(station)

    json.dump(stations, open('stations_chmino.json','w'))

if __name__=='__main__':
    main()

