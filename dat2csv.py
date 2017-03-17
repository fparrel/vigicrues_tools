#!/usr/bin/env python

import struct
import json
import datetime

serialisation='<Lf'
value_size = struct.calcsize(serialisation)

def dat2csv(station_id,min_date,nb_min=15):
    fdat=open('%s.dat'%station_id,'rb')
    fcsvfull=open('viewer/%s.csv'%station_id,'w')
    fcsvfull.write('datetime,value\n')
    fcsvlast=open('viewer/%s-last.csv'%station_id,'w')
    fcsvlast.write('datetime,value\n')
    nb_on_last = 0
    last_lines = []
    while True:
        buf=fdat.read(value_size)
        if len(buf)>0:
            timestamp,value = struct.unpack(serialisation,buf)
            csvline = '%s,%f\n'%(timestamp,value)
            fcsvfull.write(csvline)
            last_lines.append(csvline)
            last_lines=last_lines[:nb_min]
            if datetime.date.fromtimestamp(timestamp)>=min_date:
                fcsvlast.write(csvline)
                nb_on_last += 1
        else:
            break
    if nb_on_last<nb_min:
        fcsvlast.write(''.join(last_lines))
    fcsvfull.close()
    fcsvlast.close()
    fdat.close()

if __name__=='__main__':
    f=open('viewer/stations.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        dat2csv(station['id'],datetime.date.today())
