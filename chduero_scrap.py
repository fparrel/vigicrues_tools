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
    direct_url = 'http://www.saihduero.es/%s' % t[i+6:j]
    r = requests.get(direct_url)
    t = r.text.encode(r.encoding)
    i = t.find('chartData =')
    i = t.find('{',i)
    j = t.find('];',i)
    d = t[i:j]
    return filter(lambda x:x!=None,map(parsePoint,d.split('},\n'))),direct_url

def process(station_id):
    values_gen,direct_url = get_data(station_id)
    values = list(values_gen)
    if len(values)>0:
        save_values('chduero','debit_%s'%station_id,values)
    return direct_url

def main():
    f = open('stations_chduero.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        print station['station'].encode('utf8')
        direct_url = process(station['id'])
        if station.has_key('direct_url'):
            if station['direct_url'] != direct_url:
                print 'direct_url different!'
        else:
            station['direct_url'] = direct_url
    f = open('stations_chduero.json','w')
    json.dump(stations, f)
    f.close()

if __name__=='__main__':
    main()

