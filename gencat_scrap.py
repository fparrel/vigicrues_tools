#!/usr/bin/env python

from serialize import saveValues, loadStations
import time
import requests
import datetime

def parsePoint(dic):
    return datetime.datetime.strptime(dic['timestamp'],'%d/%m/%YT%H:%M:%S'), float(dic['value'])

def process(station, epoch):
    url = 'http://aca-web.gencat.cat/sentilo-catalog-web/admin/sensor/lastObs/AFORAMENT-EST.%(component)s.%(sensor)s/?ts=%(timestamp_ms)d' % { 'component': station['station_id'], 'sensor': station['senal_id'], 'timestamp_ms': epoch*1000 }
    print(url)
    r = requests.get(url)
    values = map(parsePoint,r.json())
    if len(values) > 0:
        saveValues('gencat', station['senal_id'], values)

def main():
    stations = loadStations('gencat')
    print('Loaded %d stations'%len(stations))
    epoch = int(time.time())
    for station in stations:
        process(station, epoch)

if __name__=='__main__':
    main()

