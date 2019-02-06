#!/usr/bin/env python

import requests
import datetime
from lxml import etree
import json
from serialize import save_values

def loadStations():
    f = open('stations_chgalicia.json','r')
    stations = json.load(f)
    f.close()
    return stations

def main():
    stations = loadStations()
    for station in stations:
        date1 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1),'%d/%m/%Y')
        date2 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=-1),'%d/%m/%Y')
        url = 'http://www2.meteogalicia.es/servizos/AugasdeGalicia/DatosHistoricosTaboas_dezminutal.asp?est=%(id)s&param=101&data1=%(date1)s&data2=%(date2)s'%{'id':station['id'],'date1':date1,'date2':date2}
        print(url)
        r = requests.get(url)
        html = r.text.encode(r.encoding)
        t = etree.HTML(html)
        values = []
        for tr in t.xpath('//table[@class="datos"]/tr'):
            de,ke,ve = tr.xpath('th/span')
            d = datetime.datetime.strptime(de.text.strip(),'%Y-%m-%d %H:%M:%S')
            v = float(ve.text.replace(',','.'))
            values.append((d,v))
        if len(values)>0:
            save_values('chgalicia',station['id'],values)

if __name__=='__main__':
    main()
