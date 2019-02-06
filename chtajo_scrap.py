#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import xml.etree.ElementTree as ET
import datetime
from serialize import save_values
import json

def parseDate(input):
    if len(input)>10:
        return datetime.datetime.strptime(input, '%d/%m/%Y %H:%M')
    else:
        return datetime.datetime.strptime(input, '%d/%m/%Y')

def getLastValues(code_station):
    date_start_s = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=1), '%Y-%m-%d-%H-%M')
    date_end_s = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), '%Y-%m-%d-%H-%M')
    url = 'https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/origen:60m/fecha_ini:%(date_start)s/fecha_fin:%(date_end)s/zoom_ini:%(date_start)s/zoom_fin:%(date_end)s/_senal:%(code_station)sFICT98/_valor:NOR/ver_detalle:1' % {'code_station': code_station, 'date_start': date_start_s, 'date_end': date_end_s}
    print(url)
    r = requests.get(url, verify=False)
    t = r.text.encode(r.encoding)
    html = ET.fromstring(t.replace('repeat', '').replace('<br>', '<br/>'))
    for tr in html.findall('./div/table/tbody/tr'):
        tds = list(map(lambda x: x.text, tr.findall('td')))
        if tds[1] != None: # filter empty values
            yield parseDate(tds[0]), float(tds[1].replace(',', '.'))

def process(code_station):
    values = list(getLastValues(code_station))
    values.sort(key = lambda x: x[0]) # values must be sorted for save_values algorithm
    if len(values) > 0:
        save_values('chtajo', code_station, values)

def loadStations():
    f = open('stations_chtajo.json', 'r')
    stations = json.load(f)
    f.close()
    return stations

def main():
    for station in loadStations():
        print ('%s: %s' % (station['id'],station['name'])).encode('utf8')
        process(station['id'])

if __name__=='__main__':
    main()
