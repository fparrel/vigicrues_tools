#!/usr/bin/env python

import json
import requests
from lxml import etree
import datetime
from serialize import saveValues, loadStations

def main():

    for station in loadStations('chmino'):

        # Get measures in HTML form
        tag = station['senal_id']
        url = 'http://saih.chminosil.es/index.php?url=/datos/graficas_numeros/tag:%s&historia=0'%tag
        print(url)
        r = requests.get(url,cookies={'lang':'es'})
        html = r.text.encode(r.encoding)

        # Find date / values table
        tree = etree.HTML(html)
        trs = tree.xpath('//th[.="Fecha"]/parent::tr/following::tr')

        # Parse each value of the table
        values = []
        for tr in trs:
            fecha,valor = tr.xpath('td')
            d = datetime.datetime.strptime(fecha.text,'%d/%m/%Y %H:%M')
            if valor.text.strip()=='': # ignore empty values
                continue
            v = float(valor.text.replace(',','.'))
            values.append((d,v))

        # Save data if we got something
        if len(values)>0:
            values.sort(key=lambda dv:dv[0]) # Values must be sorted for saveValue()
            saveValues('chmino','%s'%tag,values)

if __name__=='__main__':
    main()

