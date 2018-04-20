#!/usr/bin/env python

import requests
import json
import re

cumul_horare_re = re.compile(r', dernier cumul horaire ([0-9]*\.[0-9]*) mm le ([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) - ([0-9][0-9]):([0-9][0-9])')

def process(code_station):
    url = 'http://www.rdbrmc.com/hydroreel2/station.php?codestation=%d'%code_station
    print url
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    for found in cumul_horare_re.findall(t):
        cumul,dd,mm,yyyy,hour,minute = found
	print float(cumul),dd,mm,yyyy,hour,minute

if __name__=='__main__':
    process(685)
    #f=open('stations_rdbrmc.json','r')
    #stations = json.load(f)
    #f.close()
    #for station in stations:
    #    process(station['id'])

