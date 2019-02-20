#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import json
import datetime

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
        # get `param`
        date1 = datetime.datetime.now()-datetime.timedelta(days=1)
        date2 = datetime.datetime.now()+datetime.timedelta(days=1)
        dia1 = date1.strftime('%d')
        mes1 = date1.strftime('%m')
        ano1 = date1.strftime('%Y')
        dia2 = date2.strftime('%d')
        mes2 = date2.strftime('%m')
        ano2 = date2.strftime('%Y')
        url = 'http://www2.meteogalicia.es/servizos/AugasdeGalicia/contidos/sensor_periodo.asp?Nest=%s&tiporede=automaticas&periodo=1&formato=1&dia1=%s&mes1=%s&ano1=%s&dia2=%s&mes2=%s&ano2=%s&idprov=0' % (station_id,dia1,mes1,ano1,dia2,mes2,ano2)
        rs = requests.get(url)
        htmls = rs.text.encode(rs.encoding)
        ts = etree.HTML(htmls)
        station['param'] = ts.xpath('//input[@id="134medida1"]/@value')[0]
        stations.append(station)

    json.dump(stations,open('stations_chgalicia.json','w'))

if __name__=='__main__':
    main()
