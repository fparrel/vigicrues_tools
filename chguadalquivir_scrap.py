#!/usr/bin/env python

import requests
from lxml import etree
import datetime
from serialize import saveValues, loadStations
import json

def process(station):
    station_id = station['id']
    nb = station['nb']
    letter = station['letter']
    url = 'http://www.chguadalquivir.es/saih/saihhist2.aspx?s1=%s_%d%s&dia=1'%(station_id,nb,letter)
    print(url)
    r = requests.get(url)
    t = etree.XML(r.text.encode(r.encoding))
    if t.find('s1')==None or t.find('x')==None:
        print('Error with %s'%url)
        return
    s1 = map(float,t.find('s1').text.split(';'))
    x = map(lambda d:datetime.datetime.fromtimestamp(float(d)),t.find('x').text.split(';')[:-1])
    values = zip(x,s1)
    if len(values)>0:
        saveValues('chguadalquivir',station_id,values)

def main():
    stations = loadStations('chguadalquivir')
    for station in stations:
        process(station)

if __name__=='__main__':
    main()

