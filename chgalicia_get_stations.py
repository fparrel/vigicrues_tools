#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import json
import datetime

def main():

    # Get list of water flow stations ('Aforos'). We're lucky, it's in json
    url = 'http://servizos.meteogalicia.gal/rss/observacion/jsonAforos.action'
    print(url)
    r = requests.get('http://servizos.meteogalicia.gal/rss/observacion/jsonAforos.action')

    stations = []
    for aforo in r.json()['listaAforos']:

        # This field gives unit and a code, but I cannot figure what this code is for. If does'nt correspond to `param`
        #measures = []
        #for medida in aforo['listaMedidas']:
        #    if medida['unidade']=='m3/s':
        #        measures.append({'param':medida['codParametro']})
        #if len(measures)!=1:
        #    raise Exception('only handle one m3/s measure')
        #else:
        #    param = measures[0]['param']

        # Get station_id
        station_id = aforo['ide']

        # Get station description page, for getting river
        url = 'http://www2.meteogalicia.es/servizos/AugasdeGalicia/estacionsinfo.asp?nest=%d'%station_id
        print(url)
        rs = requests.get(url)
        htmls = rs.text.encode(rs.encoding)
        ts = etree.HTML(htmls)

        # Get river of station
        river = ts.xpath(u'//span[contains(.,"Estación no río")]/b')[0].text

        station = {'station_id':station_id,'lat':float(aforo['latitude']),'lon':float(aforo['lonxitude']),'name':aforo['nomeEstacion'],'river':river}

        # Get the data download form, this will give us the value of `param`
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
        print(url)
        rs = requests.get(url)
        htmls = rs.text.encode(rs.encoding)
        ts = etree.HTML(htmls)

        # 134medida1 always correspond to 'Caudal Medio da Auga'
        station['param'] = ts.xpath('//input[@id="134medida1"]/@value')[0]
        station['desc'] = 'Caudal Medio da Auga'
        station['unit'] = 'm3/s'

        station['senal_id'] = '%s-1'%station_id
        stations.append(station)

    json.dump(stations,open('stations_chgalicia.json','w'))

if __name__=='__main__':
    main()

