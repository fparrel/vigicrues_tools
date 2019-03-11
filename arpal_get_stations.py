#!/usr/bin/env python

import requests
from lxml import etree
import json
import datetime
from serialize import saveValues
import re

pat_stationid = re.compile(r'.*\[(.*)\]')

def get_all_stations():
    r = requests.get('http://93-62-155-214.ip23.fastwebnet.it/~omirl/WEB/NewIdro/idrometri.html')
    html = r.text.encode(r.encoding)
    t = etree.HTML(html)
    stations = {}
    for tr in t.xpath('//td/a/parent::td/parent::tr'):
        name = tr.xpath('td/a/text()')[0]
        empty,Localitai,Provincia,Comune,Bacino,Corso,massimo24Hm,OraUTCmassimo,ValoreOraDiRifm,OraDiRif,Tendenza=tr.xpath('td/text()')
        station_id = pat_stationid.findall(name)[0]
        stations[station_id] = {'name':name,'river':Corso,'station_id':station_id}
    stations = list(stations.itervalues())
    json.dumps(stations,open('stations_arpal.json', 'w'))

def scrap():
    r = requests.get('http://93-62-155-214.ip23.fastwebnet.it/~omirl/WEB/NewIdro/idrometri.html')
    html = r.text.encode(r.encoding)
    t = etree.HTML(html)
    for tr in t.xpath('//td/a/parent::td/parent::tr'):
        name = tr.xpath('td/a/text()')[0]
        station_id = pat_stationid.findall(name)[0]
        empty,Localitai,Provincia,Comune,Bacino,Corso,massimo24Hm,OraUTCmassimo,ValoreOraDiRifm,OraDiRif,Tendenza=tr.xpath('td/text()')
        if ValoreOraDiRifm.strip()=='--':
            continue
        value = float(ValoreOraDiRifm)
        when = datetime.datetime.strptime(OraDiRif,'%d/%m/%Y %H:%M')
        print station_id
        saveValues('arpal',station_id,[(when,value)])

def main():
    get_all_stations()
    scrap()

if __name__=='__main__':
    main()

