#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests #for http requests
import datetime #for datetime parsing
import json
from serialize import save_values


def process(station_id):
    url = 'https://www.vigicrues.gouv.fr/services/observations.json/index.php?CdStationHydro=%(station_id)s&GrdSerie=H&FormatSortie=simple'%{'station_id':station_id}
    print url
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    values = map(lambda timestampvalue: [datetime.datetime.fromtimestamp(timestampvalue[0]/1000),timestampvalue[1]],json.loads(t)['Serie']['ObssHydro'])
    print station_id,'H',len(values)
    if len(values)>0:
        save_values('vigicrues',station_id,values)
    url = 'https://www.vigicrues.gouv.fr/services/observations.json/index.php?CdStationHydro=%(station_id)s&GrdSerie=Q&FormatSortie=simple'%{'station_id':station_id}
    print url
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    values = map(lambda timestampvalue: [datetime.datetime.fromtimestamp(timestampvalue[0]/1000),timestampvalue[1]],json.loads(t)['Serie']['ObssHydro'])
    print station_id,'Q',len(values)
    if len(values)>0:
        save_values('vigicrues','%s-q'%station_id,values) 

if __name__=='__main__':
    f=open('stations.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        process(station['id'])
