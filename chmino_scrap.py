#!/usr/bin/env python

import json
import requests
from lxml import etree
import datetime
from serialize import saveValues, loadStations

def main():
    for station in loadStations('chmino'):
        print(station['id'])
        for tag in station['tags']:
            url = 'http://saih.chminosil.es/index.php?url=/datos/graficas_numeros/tag:%s&historia=0'%tag
            print(url)
            r = requests.get(url,cookies={'lang':'es'})
            html = r.text.encode(r.encoding)
            tree = etree.HTML(html)
            trs = tree.xpath('//th[.="Fecha"]/parent::tr/following::tr')
            values = []
            for tr in trs:
                fecha,valor = tr.xpath('td')
                d = datetime.datetime.strptime(fecha.text,'%d/%m/%Y %H:%M')
                try:
                    v = float(valor.text.replace(',','.'))
                except: #in case of empty value
                    print('Warning: cannot convert for %s'%url)
                    continue
                values.append((d,v))
            if len(values)>0:
                values.sort(key=lambda dv:dv[0])
                saveValues('chmino','%s'%tag,values)

if __name__=='__main__':
    main()

