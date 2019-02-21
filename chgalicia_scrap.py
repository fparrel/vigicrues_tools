#!/usr/bin/env python

import requests
import datetime
import json
from serialize import saveValues, loadStations
import re

chgalicia_pat = re.compile(r'\s*[0-9]\s*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})\s+Caudal Medio da Auga \(m3/s\)\s+([0-9,]+)')

def parseValue(txt):
    return datetime.datetime.strptime(txt[0],'%Y-%m-%d %H:%M:%S'), float(txt[1].replace(',','.'))

def main():
    stations = loadStations('chgalicia')
    for station in stations:
        date1 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1),'%d/%m/%Y')
        date2 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=-1),'%d/%m/%Y')
        url = 'http://www2.meteogalicia.es/servizos/AugasdeGalicia/contidos/historicos_descarga.asp?Nest=%s&param=%s&periodo=1&data1=%s&data2=%s&formato=1' % (station['id'], station['param'], date1, date2)
        print(url)
        r = requests.get(url)
        txt = r.text.encode(r.encoding)
        values_text = chgalicia_pat.findall(txt)
        values = filter(lambda tv:tv[1]!=-9999.0,map(parseValue,values_text))
        if len(values)>0:
            saveValues('chgalicia',station['id'],values)

if __name__=='__main__':
    main()

