#!/usr/bin/env python

import requests
import yaml
import json

r = requests.get('http://www.saihduero.es/risr')
t = r.text.encode(r.encoding)
i = t.find('datosAF =')
i = t.find('{',i)
j = t.find(');',i)
datos = '['+t[i:j].replace('\t','')+']'
print datos
stations = yaml.load(datos)
json.dump(stations,open('stations_chduero.json','w'))

