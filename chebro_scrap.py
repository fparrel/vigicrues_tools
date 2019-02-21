#!/usr/bin/env python

import json
import requests
import datetime
import re
from serialize import saveValues, loadStations

def main():
    pat = re.compile(r"<tr><td class='_lineas' >([^<]*)<..td><td class=.._lineas.. style=..text-align:right;..>([^<]*)<..td><..tr>")

    for station in loadStations('chebro'):
      if station['tag']=='':
          continue
      print(station['id'])
      date_start_s = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1),'%Y-%m-%d-%H-%M')
      date_end_s = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=-1),'%Y-%m-%d-%H-%M')
      url = 'http://195.55.247.237/saihebro/views/elements/graficas/ajax.php?url=/sedh/ajax_obtener_datos_numericos/fecha_ini:%s/fecha_fin:%s/intervalo_hora:0/intervalo_15m:1/fecha:%s/_senal:%s'%(date_start_s,date_end_s,date_end_s,station['tag'])
      print(url)
      r = requests.get(url)
      points = pat.findall(r.text)
      values = list(map(lambda p: (datetime.datetime.strptime(p[0],'%d\\/%m\\/%Y %H:%M'),float(p[1].replace('.','').replace(',','.'))),filter(lambda p: p[1]!='',points)))
      values.sort(key=lambda x:x[0]) # values must be sorted for saveValues algorithm
      if len(values)>0:
          saveValues('chebro','%s'%station['id'],values)

if __name__=='__main__':
    main()

