#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import yaml
import json
from lxml import etree

unitsbydefault = {'Nivel':'m','Caudal':'m3/s','Temperatura ambiente':'ºC'}
senal_name2id = {'Nivel':0,'Caudal':1,'Caudal vertido':2,'Temperatura ambiente':3,u'Pluviometr\xeda':4}

def getSenales(station_id):
      # This url changes sometimes
      url = 'http://www.saihduero.es/ficha-risr?r=%s' % station_id
      print(url)
      r = requests.get(url)
      html = r.text.encode(r.encoding)
      tree = etree.HTML(html)
      for tr in tree.xpath('//th[.="Variable"]/parent::tr/parent::thead/following::tbody')[0].xpath('tr'):
          name = tr.xpath('td/text()')[0]
          units = tr.xpath('td/span/text()')
          if len(units)==0:
              unit = unitsbydefault[name]
          else:
              unit = units[0]
          href = tr.xpath('td/a/@href')[0]
          yield name,unit,href

def main():
    url = 'http://www.saihduero.es/risr'
    print(url)
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    # Find datos in javascript format
    i = t.find('datosAF =')
    i = t.find('{',i)
    j = t.find(');',i)
    datos = '['+t[i:j].replace('\t','')+']'
    stations_in = yaml.load(datos)
    stations_out = []
    # example: { id: 'EA153', station: 'La Fuentona, 2153', river: 'Abión', lat: 41.73043292, lng: -2.85761050, date: '21 feb', time: '00:00', n: '0,76 m', q: '0,68 m3/s', n_status: 'variable_normal', q_status: 'variable_normal', status: 'normal', clazz: 5 }
    # Rename and select fields
    for station in stations_in:
        for name,unit,href in getSenales(station['id']):
            stations_out.append({'station_id':station['id'],'senal_id':'%s-%d'%(station['id'],senal_name2id[name]), 'name':station['station'], 'river':station['river'], 'lat':station['lat'], 'lon':station['lng'], 'unit': unit, 'desc':name, 'direct_url':'http://www.saihduero.es/%s'%href})
    json.dump(stations_out,open('stations_chduero.json','w'))

if __name__=='__main__':
    main()

