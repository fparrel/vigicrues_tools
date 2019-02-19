#!/usr/bin/env python

import requests
from lxml import etree
import datetime
from serialize import save_values
import json

def loadStations():
    f = open('stations_chguadalquivir.json','r')
    stations = json.load(f)
    f.close()
    return stations

def process(station):
    station_id = station['id']
    print station_id
    nb = station['nb']
    letter = station['letter']
    url = 'http://www.chguadalquivir.es/saih/saihhist2.aspx?s1=%s_%d%s&dia=1'%(station_id,nb,letter)
    r = requests.get(url)
    t = etree.XML(r.text.encode(r.encoding))
    if t.find('s1')==None or t.find('x')==None:
        print 'Error with %s'%url
        return
    print t.find('descr').text
    s1 = map(float,t.find('s1').text.split(';'))
    x = map(lambda d:datetime.datetime.fromtimestamp(float(d)),t.find('x').text.split(';')[:-1])
    values = zip(x,s1)
    if len(values)>0:
        save_values('chguadalquivir',station_id,values)

def main():
    stations = loadStations()
    for station in stations:
        process(station)

if __name__=='__main__':
    main()

