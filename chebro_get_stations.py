#!/usr/bin/env python

import requests
import re
import json
import utm

pat = re.compile(r"<option value='([^']*)'>([^<]*)</option>")

def getHtml():
  r = requests.get('http://195.55.247.237/saihebro/index.php?url=/datos/mapas/tipoestacion:A')
  return r.text.encode(r.encoding)

def getOptions(html):
  idx = html.find("<option value='' selected='selected'>(Localizar estaci&oacute;n)</option>")
  idx2 = html.find("</select>", idx)
  return html[idx:idx2]

def getStationDataHtml(station_id):
  r = requests.get('http://195.55.247.237/saihebro/index.php?url=/datos/ficha/estacion:%s'%station_id)
  return r.text.encode(r.encoding)

def parseStation(html):
  idx = html.find('<a href="javascript:cambiarCapa(1,4,\'ficha\');" >')
  idx2 = html.find('</a>', idx)
  desc = html[idx+len('<a href="javascript:cambiarCapa(1,4,\'ficha\');" >'):idx2]
  print(desc)
  idx = html.find('<td class="celdacn">Z</td>',idx2)
  idx = html.find('<td class="celdac" colspan="2">',idx)
  idx2 = html.find('</td>',idx)
  h = int(html[idx+len('<td class="celdac" colspan="2">'):idx2])
  idx = html.find('<td class="celdac">',idx2)
  idx2 = html.find('</td>',idx)
  x = float(html[idx+len('<td class="celdac">'):idx2].replace(',','.'))
  idx = html.find('<td class="celdac">',idx2)
  idx2 = html.find('</td>',idx)
  y = float(html[idx+len('<td class="celdac">'):idx2].replace(',','.'))
  idx = html.find('<td class="celdac">',idx2)
  idx2 = html.find('</td>',idx)
  z = float(html[idx+len('<td class="celdac">'):idx2].replace(',','.'))
  idx = html.find('<td class="celdaln" colspan="5">R&iacute;o:</td>')
  idx = html.find('<td class="celdal" colspan="5">',idx)
  idx2 = html.find('</td>',idx)
  river = html[idx+len('<td class="celdal" colspan="5">'):idx2]
  print(river)
  idx = html.find('<td class="celdal">CAUDAL',idx2)
  idx = html.find('index.php?url=/datos/graficas/tag:', idx)
  idx2 = html.find('"', idx)
  tag = html[idx+len('index.php?url=/datos/graficas/tag:'):idx2]
  if (len(tag)>100):
    tag = ''  
  print(tag)
  return desc,h,x,y,z,river,tag

def main():
  html = getHtml()
  options = getOptions(html)
  values = pat.findall(options)
  stations = []
  for v,t in values:
    station_id,zone,station_type = v.split('|')
    print(station_id)
    name = ' '.join(t.replace('&nbsp;',' ').split()[1:])
    desc,h,x,y,z,river,tag = parseStation(getStationDataHtml(station_id))
    lat,lon = utm.to_latlon(x,y,h,'T')
    stations.append({'id':station_id,'tag':tag,'zone':zone,'type':station_type,'name':name,'desc':desc,'utm_x':x,'utm_y':y,'alt':z,'river':river,'lat':lat,'lon':lon})
  json.dump(stations,open('stations_chebro.json','w'))

if __name__=='__main__':
  main()
