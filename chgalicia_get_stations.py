#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import json

def main():
    stations = []
    r = requests.get('http://servizos.meteogalicia.gal/rss/observacion/jsonAforos.action')
    for aforo in r.json()['listaAforos']:
        #measures = []
        #for medida in aforo['listaMedidas']:
        #    if medida['unidade']=='m3/s':
        #        measures.append({'param':medida['codParametro']})
        #if len(measures)!=1:
        #    raise Exception('only handle one m3/s measure')
        #else:
        #    param = measures[0]['param']
        station_id = aforo['ide']
        rs = requests.get('http://www2.meteogalicia.es/servizos/AugasdeGalicia/estacionsinfo.asp?nest=%d'%station_id)
        htmls = rs.text.encode(rs.encoding)
        ts = etree.HTML(htmls)
        river = ts.xpath(u'//span[contains(.,"Estación no río")]/b')[0].text
        station = {'id':station_id,'lat':float(aforo['latitude']),'lon':float(aforo['lonxitude']),'name':aforo['nomeEstacion'],'river':river}
        stations.append(station)

    json.dump(stations,open('stations_chgalicia.json','w'))

if __name__=='__main__':
    main()
