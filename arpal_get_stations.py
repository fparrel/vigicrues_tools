#!/usr/bin/env python

import requests
from lxml import etree
import json
import datetime
from serialize import saveValues
import re

pat_stationid = re.compile(r'.*\[(.*)\]')

def getGeos():
    url = 'http://93.62.155.214/~omirl/WEB/omirl.xml'
    print(url)
    r = requests.get(url)
    t = etree.XML(r.text.encode(r.encoding))
    geos = {}
    for marker in t:
        geos[marker.attrib['code']] = marker.attrib
    return geos

def listStations():
    url = 'http://93-62-155-214.ip23.fastwebnet.it/~omirl/WEB/NewIdro/idrometri.html'
    print(url)
    r = requests.get(url)
    html = r.text.encode(r.encoding)
    t = etree.HTML(html)
    for tr in t.xpath('//td/a/parent::td/parent::tr'):
        name = tr.xpath('td/a/text()')[0]
        code1 = pat_stationid.findall(name)[0]
        code2 = tr.xpath('td/a/@href')[0].lstrip("javascript:aprigrafico('").rstrip("');")
        empty,Localitai,Provincia,Comune,Bacino,Corso,massimo24Hm,OraUTCmassimo,ValoreOraDiRifm,OraDiRif,Tendenza=tr.xpath('td/text()')
        yield name,code1,code2,Corso,ValoreOraDiRifm,OraDiRif

def getAllStations():
    geos = getGeos()
    stations = {}
    for name,code1,code2,river,value,when in listStations():
        geo = geos[code2]
        stations[code2] = {'name':name,'river':river.strip(),'station_id':code1,'senal_id':code2,'alt':int(geo['elev']),'lat':float(geo['lat']),'lon':float(geo['lon'])}
    stations = list(stations.itervalues())
    json.dump(stations,open('stations_arpal.json', 'w'))

def scrap():
    already_done = []
    for name,code1,code2,river,value,when in listStations():
        if value.strip()=='--':
            continue
        if code2 in already_done:
            continue
        already_done.append(code2)
        value = float(value)
        when = datetime.datetime.strptime(when,'%d/%m/%Y %H:%M')
        print(code2)
        saveValues('arpal',code1,[(when,value)])

def main():
    getAllStations()

if __name__=='__main__':
    main()

