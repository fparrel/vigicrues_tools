#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import requests
import demjson
import datetime
from serialize import saveValues, loadStations

def process(station):

    # Get measure chart page
    url = 'http://www.redhidrosurmedioambiente.es/saih/mapa/tiempo/real/grafica/%s'%station['senal_id']
    print(url)
    r = requests.get(url)
    html = r.text.encode(r.encoding)

    # Look for chart data in the javacript, and parse it
    i = html.find('var lineChartData = {')
    if i==-1:
        i = html.find('var barChartData = {')
    if i==-1:
        raise Exception('data not found')
    j = html.find('};',i)
    if j==-1:
        raise Exception('data not found')
    chartdata = demjson.decode(html[i+19:j+1]) # 19: ok for both bar or line

    # Parse datetimes
    ts = map(lambda s:datetime.datetime.strptime(s,'%d/%m/%y %H:%M'), chartdata['labels'])

    # Find the right data set (other data sets are alerting levels)
    if len(chartdata['datasets'])==1: # only one dataset, use it
        vs = map(float,chartdata['datasets'][0]['data'])
    else: # several datasets, select the right one
        for d in chartdata['datasets']:
            lbl = d['label']
            if lbl.startswith('NIVEL') or lbl.startswith(u'Precipitación horaria'):
                vs = map(float,d['data'])
                break

    # Merge datetimes and values
    values = zip(ts,vs)

    # Save values if we got something
    if len(values)>0:
        saveValues('hidrosur',station['senal_id'],values)

def main():
    stations = loadStations('hidrosur')
    for station in stations:
        process(station)

if __name__=='__main__':
    main()

