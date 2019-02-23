#!/usr/bin/env python

import requests
import datetime
from serialize import saveValues, loadStations
import re

chgalicia_pat = re.compile(r'\s*[0-9]\s*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})\s+Caudal Medio da Auga \(m3/s\)\s+([0-9,]+)')

def parseValue(txt):
    return datetime.datetime.strptime(txt[0],'%Y-%m-%d %H:%M:%S'), float(txt[1].replace(',','.'))

def main():

    stations = loadStations('chgalicia')

    for station in stations:

        # Get measures in text format
        date1 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1),'%d/%m/%Y')
        date2 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=-1),'%d/%m/%Y')
        url = 'http://www2.meteogalicia.es/servizos/AugasdeGalicia/contidos/historicos_descarga.asp?Nest=%s&param=%s&periodo=1&data1=%s&data2=%s&formato=1' % (station['station_id'], station['param'], date1, date2)
        print(url)
        r = requests.get(url)
        txt = r.text.encode(r.encoding)

        # Find measures with a regex
        values_text = chgalicia_pat.findall(txt)

        # Filter invalid values: -9999.0
        values = filter(lambda tv:tv[1]!=-9999.0,map(parseValue,values_text))

        # Save values if we got something
        if len(values)>0:
            saveValues('chgalicia',station['senal_id'],values)

if __name__=='__main__':
    main()

