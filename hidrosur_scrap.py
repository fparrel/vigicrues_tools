#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import requests
import demjson
import datetime
from serialize import save_values

def loadStations():
    f = open('stations_hidrosur.json','r')
    stations = json.load(f)
    f.close()
    return stations

def process(measure):
    url = 'http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/grafica/%s'%measure['id']
    print url
    r = requests.get(url)
    html = r.text.encode(r.encoding)
    i = html.find('var lineChartData = {')
    if i==-1:
        i = html.find('var barChartData = {')
    if i==-1:
        raise Exception('data not found')
    j = html.find('};',i)
    if j==-1:
        raise Exception('data not found')
    chartdata = demjson.decode(html[i+19:j+1]) # 19: ok for both bar or line
    ts = map(lambda s:datetime.datetime.strptime(s,'%d/%m/%y %H:%M'), chartdata['labels'])
    if len(chartdata['datasets'])==1: # only one dataset, use it
        vs = map(float,chartdata['datasets'][0]['data'])
    else: # several datasets, select the right one
        for d in chartdata['datasets']:
            lbl = d['label']
            if lbl.startswith('NIVEL') or lbl.startswith(u'Precipitación horaria'):
                vs = map(float,d['data'])
                break
    values = zip(ts,vs)
    if len(values)>0:
        save_values('hidrosur',measure['id'],values)

def main():
    stations = loadStations()
    for station in stations:
        for measure in station['measures']:
            process(measure)

if __name__=='__main__':
    main()

