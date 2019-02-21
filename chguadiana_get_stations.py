#!/usr/bin/env python

import requests
from lxml import etree
import re
import json
import datetime

pat = re.compile(r'./charts/charts_tr_([a-z]+).php\?station=([A-Z0-9-]+).*\&label=([^\&]+)')

river_at = re.compile(r'(.*)(\sen\s|a\.\sab\.|a\.\sarr\.)(.*)')

prefix = 'http://www.saihguadiana.com:7080/visorTR/'

def getDescAndUnit(station):
    print(station['url'])
    r = requests.get(station['url'])
    t = etree.HTML(r.text.encode(r.encoding))
    columns = []
    for tr in t.xpath('//tr'):
        tds = tr.xpath('td')
        if len(tds)>0:
            values = dict(zip(columns,map(lambda td:td.text,tds)))
            d = datetime.datetime.strptime(values['Fecha'],'%Y-%m-%d %H:%M:%S')
            if values.has_key(u'Caudal (m\xb3/s)'):
                return 'Caudal','m3/s'
            elif values.has_key(u'Nivel (m)'):
                return 'Nivel','m'
            elif values.has_key(u'Volumen (hm\xb3)'):
                return 'Volumen','hm3'
        else:
            ths = tr.xpath('th')
            columns = map(lambda th:th.text,ths)
    return None, None

def parseStation(e):
    href = e.get('href')
    t,station_id,station_name = pat.findall(href)[0]
    url = prefix + href
    m = river_at.findall(station_name)
    if len(m)==1:
        river = m[0][0]
    else:
        river = station_name
    print(m,river)
    return {'type':t,'id':station_id,'name':station_name,'url':url,'river':river}

def main():

    r = requests.get(prefix + 'index.php')
    html = r.text.encode(r.encoding)

    tree = etree.HTML(html)

    stations = list(map(parseStation,tree.xpath('//td/a[starts-with(@href,"./charts/charts_tr_")]')))
    for station in stations:
        desc, unit = getDescAndUnit(station)
        if desc!=None and unit!=None:
            station['desc'] = desc
            station['unit'] = unit

    json.dump(stations,open('stations_chguadiana.json','w'))

if __name__=='__main__':
    main()

