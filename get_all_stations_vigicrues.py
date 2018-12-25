#!/usr/bin/env python

import requests #for http requests
import re
import json

BASSINPREFIX = 'href="./niv2-bassin.php?CdEntVigiCru='
STATIONPREFIX = 'niv3-station.php?'

EXTRACTSTATIONIDRE = re.compile('CdStationHydro=([A-Z0-9]+)')

def extract_stationid(url):
    return EXTRACTSTATIONIDRE.findall(url)[0]

def parse_page(t,prefix):
    i=0
    while i!=-1:
        i = t.find(prefix,i)
        if i==-1:
            break
        j = t.find('"', i+len(prefix))
        yield t[i:j]
        i = j

def main():
    all_stations=[]
    r = requests.get('http://www.vigicrues.gouv.fr')
    t = r.text.encode(r.encoding)
    bassins = map(lambda hrefurl: int(hrefurl[len(BASSINPREFIX):]),list(set(parse_page(t,BASSINPREFIX))))
    for bassin in bassins:
        print 'Bassin %s' % bassin
        r = requests.get('http://www.vigicrues.gouv.fr/niv2-bassin.php?CdEntVigiCru=%s'%bassin)
        t = r.text.encode(r.encoding)
        all_stations += list(map(extract_stationid,parse_page(t,STATIONPREFIX)))
    all_stations = list(set(all_stations))
    all_stations_obj = []
    for station in all_stations:
        r = requests.get('http://www.vigicrues.gouv.fr/services/station.json/index.php?CdStationHydro=%s'%station)
        all_stations_obj.append({'id':station,'river':r.json()['LbCoursEau'].encode(r.encoding),'name':r.json()['LbStationHydro'].encode(r.encoding)})
    json.dump(all_stations_obj,open('stations_vigicrues.json','w'))

if __name__=='__main__':
    main()

