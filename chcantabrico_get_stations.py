#!/usr/bin/env python

import requests
from lxml import etree
import json
try:
    from urllib.parse import urlparse
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import urlparse
    from urlparse import parse_qs

def getFlow4Level(url):
    r = requests.get(url)
    t = etree.HTML(r.text.encode(r.encoding))
    tds = t.xpath("//td")
    next_is_level = False
    next_is_flow = False
    flow = ''
    level = ''
    flow4level = {}
    for td in tds:
        if td.text==None:
            continue
        if td.text.strip() == 'Nivel del agua':
            next_is_level = True
        elif next_is_level:
            spans = td.xpath('span')
            if len(spans)>0:
                level = spans[0].text.strip()
            else:
                level = td.text.strip()
            next_is_level = False
        elif td.text.strip() == 'Caudal circulante':
            next_is_flow = True
        elif next_is_flow:
            spans = td.xpath('span')
            if len(spans)>0:
                flow = spans[0].text.strip()
            else:
                flow = td.text.strip()
            next_is_flow = False
        if flow!='' and level!='':
            if level == 'm' or flow == 'm': # some are empty
                continue
            flow4level[float(level.strip(' m'))] = float(flow.strip(' m'))
    return flow4level


def getStations():
    r = requests.get("https://www.chcantabrico.es/web/guest/caudal-circulante")
    t = etree.HTML(r.text.encode(r.encoding))
    for tr in t.xpath("//table[@class='caudales tablefixedheader']")[0].xpath('tbody/tr'):
        tds = tr.xpath("td")
        codigo = tr.xpath("td[@class='codigo']")[0]
        station_id1 = codigo.text
        rio = tds[tds.index(codigo)+1]
        links = rio.xpath("a")
        if len(links)==1:
            river = links[0].text.strip() #river is in a link
        else:
            river = rio.text.strip() #river is just test
        a = tds[tds.index(codigo)+2].xpath("a")[0]
        station_name = a.text.strip()
        url = a.get('href')
        station_id2 = parse_qs(urlparse(url).query)['cod_estacion'][0]
        flow4level = getFlow4Level(url)
        station = {'id':station_id2,'river':river,'name':station_name,'url':url,'flow4level':flow4level}
        print station
        yield station

def main():
    json.dump(list(getStations()),open("stations_chcantabrico.json","w"))

if __name__=='__main__':
    main()
