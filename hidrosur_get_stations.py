#!/usr/bin/env python

import requests
from lxml import etree
import utm
import json

def getHtmlTree(url):
    # Get and parse url as HTML
    print(url)
    r = requests.get(url)
    return etree.HTML(r.text.encode(r.encoding))

def main():

    stations = []

    # For each area
    for nb in ['ii','iii','iv','v','vi','vii']:

        # Get list of 'aforos'
        url = 'http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/subsistema/%s/aforos'%nb
        t = getHtmlTree(url)

        # Parse list of 'ficha' (=station description) of the area
        for ficha in t.xpath('//a[starts-with(@href,"http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/ficha/")]/@href'):

            # station_id is in the url
            station_id = ficha.split('/')[-1]

            # Get contents of 'ficha'
            f = getHtmlTree(ficha)

            # Parse information about this station
            name, h, x, y, z, town, river, provincia = f.xpath('//td[.="X"]/parent::tr/following::tr/td/text()')[:8]
            river = river.encode('latin1') # Encoding is latin1, convert
            name = name.encode('latin1')
            x = float(x)
            y = float(y)
            h = int(h)
            lat, lon = utm.to_latlon(x,y,h,'S') # all CH is in UTM grid zone 29S or 30S

            # Find each measure
            senales = []
            for grafica in f.xpath('//a[starts-with(@href,"http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/grafica/")]/parent::td/parent::tr'):
                # Parse measure
                senal_desc1, senal_id, value, unit = grafica.xpath('td/text()')
                unit = unit.encode('latin1')

                # Trick to get encoding: try with latin1, if not working, it mean that it's already encoded in utf8
                try:
                    senal_desc = senal_desc1.encode('latin1')
                    json.dumps(senal_desc)
                except:
                    senal_desc = senal_desc1 # already encoded

                # Add to list
                station = {'station_id': station_id, 'name': name, 'utm_x': x, 'utm_y': y, 'alt': z, 'lat': lat, \
                           'lon': lon, 'river': river, 'desc': senal_desc, 'senal_id': senal_id, 'unit': unit}
                stations.append(station)

    # Save to disk
    json.dump(stations,open('stations_hidrosur.json','w'))

if __name__=='__main__':
    main()

