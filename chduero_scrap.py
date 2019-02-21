#!/usr/bin/env python

import requests
import datetime
import json
from serialize import saveValues, loadStations
from lxml import etree

def parsePoint(p):
    try:
        s = p.split('v:')
        if s[1].endswith('}\t'):
            v = float(s[1][:-2])
        else:
            v = float(s[1])
        return datetime.datetime.strptime(s[0][4:-3],"%d/%m/%Y %H:%M"),v
    except:
        print('Could not parse: "%s"' % p)
    return None

def getData(direct_url):
    print(direct_url)
    r = requests.get(direct_url)
    t = r.text.encode(r.encoding)
    i = t.find('chartData =')
    i = t.find('{',i)
    j = t.find('];',i)
    d = t[i:j]
    return filter(lambda x: x!=None, map(parsePoint, d.split('},\n')))

def process(station):
    direct_url = station['direct_url']
    values = list(getData(direct_url))
    if len(values) > 0:
        saveValues('chduero', station['senal_id'], values)

def main():
    stations = loadStations('chduero')
    for station in stations:
        print('%s %s' % (station['name'].encode('utf8'),station['desc'].encode('utf8')))
        process(station)

if __name__=='__main__':
    main()

