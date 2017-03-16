#!/usr/bin/env python

import struct
import json

serialisation='<Lf'
value_size = struct.calcsize(serialisation)

def read(station_id):
    f=open('%s.dat'%station_id,'rb')
    while f:
        buf=f.read(value_size)
        if len(buf)>0:
            yield struct.unpack(serialisation,buf)
        else:
            break
    f.close()

def dat2csv(station_id):
    f=open('viewer/%s.csv'%station_id,'w')
    f.write('datetime,value\n')
    f.write('\n'.join(map(lambda data: '%s,%f'%(data[0],data[1]),read(station_id))))
    f.close()

if __name__=='__main__':
    f=open('viewer/stations.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        dat2csv(station['id'])
