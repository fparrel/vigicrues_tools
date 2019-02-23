#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

# http://aca-web.gencat.cat/sdim2/apirest/catalog?componentType=aforament
# http://aca-web.gencat.cat/sentilo-catalog-web/admin/sensor/lastObs/AFORAMENT-EST.%(component)s.%(sensor)s/?ts=%(timestamp_ms)d

def main():

  url = 'http://aca-web.gencat.cat/sdim2/apirest/catalog?componentType=aforament'
  print(url)
  r = requests.get(url)

  stations = []
  for sensor in r.json()['providers'][0]['sensors']:
      lat, lon = map(float,sensor['location'].split(' '))
      unit = sensor['unit']
      station_id = sensor['component']
      senal_id = sensor['sensor']
      desc = sensor['description']
      name = sensor['componentDesc']
      station = {'station_id': station_id, 'senal_id': senal_id, 'name': name, 'desc': desc, 'unit': unit}
      if sensor.has_key('componentAdditionalInfo'):
          river = sensor['componentAdditionalInfo']['Riu']
          station['river'] = river
      elif name=='Masies de Roda (Ter i Gurri)': # one 'component' / station has no river, hardcode it
          river = 'RIU GURRI'
          station['river'] = river
      else:
          print('No river for %s'%name)
      #drainage_basin_area = float(sensor['componentAdditionalInfo'][u'Superfície conca drenada'].rstrip('km²').replace(',','.'))
      stations.append(station)
  print('%d stations got'%len(stations))
  json.dump(stations,open('stations_gencat.json','w'))

if __name__=='__main__':
    main()

