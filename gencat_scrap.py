#!/usr/bin/env python

from serialize import saveValues, loadStations
import time
import requests
import datetime
import json

def parsePoint(s):
    t, v = s.split(',')
    return datetime.datetime.fromtimestamp(int(float(t))/1000), float(v)

def getPoints(ids, epoch, net):
    url = 'http://aca-web.gencat.cat/aetr/aetr2/UIL/graph.php?IDS=%s&TIPS=3&EPOCH=%d&RED=%s&UNIT=m%%B3/s' % (ids, epoch, net)
    print(url)
    r = requests.get(url)
    html = r.text.encode(r.encoding)
    i = html.find('var d0 = [[')
    j = html.find(']]',i)
    if i==-1 or j==-1:
        print('Cannot find points for %s'%url)
        return []
    return map(parsePoint,html[i+11:j].split('],['))

def process(station, epoch):
    values = getPoints(station['ids'], epoch, station['net'])
    if len(values) > 0:
        saveValues('gencat', '%s%s-%s' % (station['net'],station['id'],station['ids']), values)

def main():
    stations = loadStations('gencat')
    print('Loaded %d stations'%len(stations))
    epoch = int(time.time())
    for station in stations:
        print station['id'], station['name'].encode('utf8')
        process(station, epoch)

if __name__=='__main__':
    main()

