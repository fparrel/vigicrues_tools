#!/usr/bin/env python

import json
import requests
import datetime
import re
from serialize import save_values

f = open('stations_chebro.json','r')
stations = json.load(f)
f.close()

pat = re.compile(r"<tr><td class='_lineas' >([^<]*)<..td><td class=.._lineas.. style=..text-align:right;..>([^<]*)<..td><..tr>")

for station in stations:
  if station['tag']=='':
    continue
  print station['id']
  date_start_s = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1),'%Y-%m-%d-%H-%M')
  date_end_s = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=-1),'%Y-%m-%d-%H-%M')
  r = requests.get('http://195.55.247.237/saihebro/views/elements/graficas/ajax.php?url=/sedh/ajax_obtener_datos_numericos/fecha_ini:%s/fecha_fin:%s/intervalo_hora:0/intervalo_15m:1/fecha:%s/_senal:%s'%(date_start_s,date_end_s,date_end_s,station['tag']))
  points = pat.findall(r.text)
  values = list(map(lambda p: (datetime.datetime.strptime(p[0],'%d\\/%m\\/%Y %H:%M'),float(p[1].replace(',','.'))),filter(lambda p: p[1]!='',points)))
  values.sort(key=lambda x:x[0]) # values must be sorted for save_values algorithm
  if len(values)>0:
    save_values('chebro','%s'%station['id'],values)

