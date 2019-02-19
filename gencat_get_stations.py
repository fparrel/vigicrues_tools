#!/usr/bin/env python

import requests
import json
import utm
from lxml import etree
try:
    from urllib.parse import urlparse
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import urlparse
    from urlparse import parse_qs

def main():
  url = 'http://aca-web.gencat.cat/aetr/aetr2/BLL/visor/getStations.php'
  r = requests.post(url,{'type':'Aforament'})
  t = r.text.encode(r.encoding)
  s = t.split('#')
  stations = {}
  for i in range(0,int(s[0])):
    path, y, x, name, net, a, b = s[1+i*7:1+i*7+7]
    print name
    s2 = path.split('&')
    station_id = s2[0].lstrip('ID=')
    x = float(x)
    y = float(y)
    lat,lon = utm.to_latlon(x,y,31,'T') # all catalunya is in UTM 31T
    url = 'http://aca-web.gencat.cat/aetr/aetr2/UIL/content/contingut_station_data.php?ID=%s&NET=%s&TYPE=Aforament&reset=true' % (station_id, net)
    r = requests.get(url)
    html = r.text.encode(r.encoding)
    tree = etree.HTML(html)
    river = tree.xpath("//b[contains(text(),'Riu :')]/parent::li/text()")[0].strip()
    graph_url = tree.xpath("//iframe[@id='ifrcontent']/@src")[0]
    ids = parse_qs(urlparse(graph_url).query)['IDS'][0]
    # there are duplicates
    stations[path] = {'id':station_id,'utm_x':x,'utm_y':y,'lat':lat,'lon':lon,'net':net,'name':name,'river':river,'url':graph_url,'ids':ids}
  json.dump(list(stations.itervalues()),open('stations_gencat.json','w'))

if __name__=='__main__':
  main()

