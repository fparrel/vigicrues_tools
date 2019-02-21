#!/usr/bin/env python

import json
import requests
from lxml import etree
import datetime
from serialize import saveValues, loadStations

def getData(station):
    r = requests.get(station['url'])
    t = etree.HTML(r.text.encode(r.encoding))
    columns = []
    for tr in t.xpath('//tr'):
        tds = tr.xpath('td')
        if len(tds)>0:
            values = dict(zip(columns,map(lambda td:td.text,tds)))
            d = datetime.datetime.strptime(values['Fecha'],'%Y-%m-%d %H:%M:%S')
            if values.has_key(u'Caudal (m\xb3/s)'):
                yield d,float(values[u'Caudal (m\xb3/s)'])
            elif values.has_key(u'Nivel (m)'):
                yield d,float(values[u'Nivel (m)'])
            elif values.has_key(u'Volumen (hm\xb3)'):
                yield d,float(values[u'Volumen (hm\xb3)'])
        else:
            ths = tr.xpath('th')
            columns = map(lambda th:th.text,ths)

def main():
    for station in loadStations('chguadiana'):
        print(station['id'])
        values = list(getData(station))
        if len(values)>0:
            values.sort(key=lambda x:x[0]) # values must be sorted for saveValues algorithm
            saveValues('chguadiana','%(type)s_%(id)s'%station,values)

if __name__=='__main__':
    main()

