#!/usr/bin/env python

import json
import requests
import utm
import re

f = open('stations_chtajo.json','r')
stations = json.load(f)
f.close()

r = requests.get('http://ceh-flumen64.cedex.es/hidraulica/SAIH/r%C3%ADos_Tajo.htm')
t = r.text.encode(r.encoding)
#nums = map(float,re.compile(r'x:num="(\d+\.\d+)"').findall(t))
# ^ some are empty, so use the one below
nums = map(float,re.compile(r'">(\d+)<').findall(t))
print len(nums)
i = 0
s = {}
for id in re.compile(r'AR\d\d').findall(t):
    x = nums[i]
    y = nums[i+1]
    print id,x,y
    lat,lon = utm.to_latlon(x,y,30,'T')
    i += 2
    for station in stations:
        if station['id']==id:
            station['lat'] = lat
            station['lon'] = lon

f = open('stations_chtajo.json','w')
json.dump(stations, f)
f.close()

