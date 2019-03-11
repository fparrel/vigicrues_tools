#!/usr/bin/env python

from serialize import loadStations, saveValues
import datetime
import requests
import yaml

def getData(url):
    print(url)
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    i = t.find('data:')
    if i==-1:
        raise Exception('Cannot find begin')
    j = t.find('}',i)
    if j==-1:
        raise Exception('Cannot find end')
    return yaml.load('{'+t[i:j]+'}')

def main():
    stations = loadStations('arpapiemonte')
    for station in stations:
        d = getData(station['url'])
        if len(d)>0:
            saveValues('arpapiemonte',station['station_id'],filter(lambda dv:dv[1]!=None,map(lambda dv: (datetime.datetime.fromtimestamp(dv[0]/1000.0),dv[1]),d['data'])))

if __name__=='__main__':
    main()

