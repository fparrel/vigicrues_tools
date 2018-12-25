#!/usr/bin/env python

import requests
import datetime
import json
from serialize import save_values, get_lastupdatetime

def parsePoint(p):
    try:
        s = p.split('v:')
        if s[1].endswith('}\t'):
            v = float(s[1][:-2])
        else:
            v = float(s[1])
        return datetime.datetime.strptime(s[0][4:-3],"%d/%m/%Y %H:%M"),v
    except:
        print 'Could not parse:',p
    return None

def get_data(station_id):
    r = requests.get('http://www.saihduero.es/ficha-risr?r=%s'%station_id)
    t = r.text.encode(r.encoding)
    i = t.find('<td>Caudal</td>')
    i = t.find('href=',i)
    j = t.find('"',i+6)
    url = 'http://www.saihduero.es/%s' % t[i+6:j]
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    i = t.find('chartData =')
    i = t.find('{',i)
    j = t.find('];',i)
    d = t[i:j]
    return filter(lambda x:x!=None,map(parsePoint,d.split('},\n')))

def process(station_id):
    values = list(get_data(station_id))
    if len(values)>0:
        save_values('chduero','debit_%s'%station_id,values)

def main():
    f = open('stations_chduero.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        print station['station'].encode('utf8')
        process(station['id'])

if __name__=='__main__':
    main()

