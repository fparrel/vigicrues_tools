#!/usr/bin/env python

import requests
from lxml import etree
import re
import json

pat = re.compile(r'./charts/charts_tr_([a-z]+).php\?station=([A-Z0-9-]+).*\&label=([^\&]+)')

prefix = 'http://www.saihguadiana.com:7080/visorTR/'

r = requests.get(prefix + 'index.php')
html = r.text.encode(r.encoding)

tree = etree.HTML(html)

def parseStation(e):
    href = e.get('href')
    t,station_id,station_name = pat.findall(href)[0]
    url = prefix + href
    return {'type':t,'id':station_id,'name':station_name,'url':url}

links = map(parseStation,tree.xpath('//td/a[starts-with(@href,"./charts/charts_tr_")]'))

json.dump(list(links),open('stations_chguadiana.json','w'))
